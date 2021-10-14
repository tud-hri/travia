"""
Copyright 2020, Olger Siebinga (o.siebinga@tudelft.nl)

This file is part of Travia.

Travia is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Travia is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Travia.  If not, see <https://www.gnu.org/licenses/>.
"""
import datetime
import multiprocessing
import os

import numpy as np
import pyqtgraph
from PyQt5 import QtWidgets, QtCore, QtGui

from dataobjects import HighDDataset, Annotation, Vehicle, AnnotationType
from dataobjects.enums import DataSource
from processing.examplecost import cost_function
from visualisation import VisualisationMaster, HighDVisualisationMaster
from .annotationgraphics import AnnotationGraphicsObject
from .guimainwindow_ui import Ui_MainWindow
from .legenddialog import LegendDialog
from .worldview import WorldView
from gui.widgets import PNeumaInfoWidget, NGSimInfoWidget, HighDInfoWidget, ExidInfoWidget, VehicleInfoWidget


class TrafficVisualizerGui(QtWidgets.QMainWindow):
    selected_annotation_graphics: AnnotationGraphicsObject
    selected_annotation: Annotation
    selected_vehicle: Vehicle
    visualisation_master: VisualisationMaster
    vehicle_info_widget: VehicleInfoWidget

    def __init__(self, dataset, parent=None):
        super().__init__(parent)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.visualisation_master = None
        self.dataset_id = dataset.dataset_id
        self.view = WorldView(self, dataset.dataset_id, dataset)
        self.ui.graphicsFrame.layout().addWidget(self.view)

        self.ui.actionColor_legend.triggered.connect(lambda: LegendDialog(parent=self))
        self.ui.actionSave_current_scene_to_image.triggered.connect(self.save_current_scene)

        self.annotation_display_checkboxes = {}
        self.plot_dialogs = []

        self.ego_object = None
        self.start_time = 0
        self.end_time = 0

        self.annotation_scene = None
        self._init_annotation_drawings()

        self.annotating_active = False
        self.current_new_annotation = None

        self.selected_annotation = None
        self.selected_annotation_graphics = None
        self.selected_vehicle = None
        self.selected_invisible_vehicle_id = None
        self.overlay_visible = False

        self.vehicles = {}

        self.ui.playButton.clicked.connect(self.toggle_play)
        self.ui.recordPushButton.clicked.connect(lambda: self.toggle_play(record=True))
        self.ui.fastForwardButton.clicked.connect(self.fast_forward)
        self.ui.rewindButton.clicked.connect(self.reverse)
        self.ui.timeSlider.sliderMoved.connect(self.set_time)
        if self.dataset_id.data_source is DataSource.PNEUMA:
            # dragging the time slider does not work with pNeuma due to the way its data is stored
            self.ui.timeSlider.setEnabled(False)

        self.ui.startAnnotationPushButton.clicked.connect(self.start_annotation)
        self.ui.stopAnnotationPushButton.clicked.connect(self.stop_annotation)

        self.ui.nextFramePushButton.clicked.connect(lambda: self.step_frame(1))
        self.ui.previousFramePushButton.clicked.connect(lambda: self.step_frame(-1))
        self.ui.createPlotsPushButton.clicked.connect(self._create_plots)
        self.ui.createOverlayPushButton.clicked.connect(self._toggle_overlay)

        self.ui.annotationLastFrameSpinBox.valueChanged.connect(self._save_annotation_changes)
        self.ui.annotationFirstFrameSpinBox.valueChanged.connect(self._save_annotation_changes)
        self.ui.annotationEgoCarComboBox.currentIndexChanged.connect(self._save_annotation_changes)
        self.ui.annotationNoteLineEdit.textChanged.connect(self._save_annotation_changes)

        self.vehicle_info_widget = None
        self._initialize_vehicle_info_widget()
        self._initialize_annotation_checkboxes()

        self.update_buttons()
        self.vehicle_info_widget.enable_all_fields(False)
        self._update_annotation_info()
        self.show()

    def register_visualisation_master(self, sim_master):
        self.visualisation_master = sim_master
        self.end_time = sim_master.end_time
        self.start_time = sim_master.start_time
        self.restore_annotations()
        self.update_buttons()

        for vehicle_id in self.visualisation_master.get_all_vehicle_ids():
            self.ui.annotationEgoCarComboBox.addItem(str(vehicle_id), vehicle_id)

    def _initialize_vehicle_info_widget(self):
        if self.dataset_id.data_source == DataSource.HIGHD:
            self.vehicle_info_widget = HighDInfoWidget(parent=self)
        elif self.dataset_id.data_source == DataSource.NGSIM:
            self.vehicle_info_widget = NGSimInfoWidget(parent=self)
        elif self.dataset_id.data_source == DataSource.PNEUMA:
            self.vehicle_info_widget = PNeumaInfoWidget(parent=self)
        elif self.dataset_id.data_source == DataSource.EXID:
            self.vehicle_info_widget = ExidInfoWidget(parent=self)
        else:
            raise ValueError('No alternative is implemented for this data source. Is it a new data source?')

        self.ui.selectedVehicleInfoFrame.layout().addWidget(self.vehicle_info_widget)

    def _initialize_annotation_checkboxes(self):
        for annotation_type in AnnotationType:
            checkbox = QtWidgets.QCheckBox(str(annotation_type))
            self.ui.displayCheckboxesGroupBox.layout().addWidget(checkbox)
            checkbox.setChecked(True)
            self.annotation_display_checkboxes[annotation_type] = checkbox
            checkbox.stateChanged.connect(self._update_annotation_view)

    def _init_annotation_drawings(self):
        start_line = QtWidgets.QGraphicsLineItem(0.0, 0.0, 0.0, 1.0)
        end_line = QtWidgets.QGraphicsLineItem(1000.0, 0.0, 1000.0, 1.0)
        self.annotation_scene = QtWidgets.QGraphicsScene()
        self.ui.annotationGraphicsView.setScene(self.annotation_scene)
        self.ui.annotationGraphicsView.scene().addItem(start_line)
        self.ui.annotationGraphicsView.scene().addItem(end_line)
        view_rect = QtCore.QRectF(0.0, 0.0, self.ui.annotationGraphicsView.scene().itemsBoundingRect().width(), 1.0)
        self.ui.annotationGraphicsView.fitInView(view_rect, QtCore.Qt.KeepAspectRatio)

    def _update_annotation_view(self):
        for existing_annotation_graphics in self.ui.annotationGraphicsView.items():
            if isinstance(existing_annotation_graphics, AnnotationGraphicsObject):
                annotation_type = existing_annotation_graphics.annotation.annotation_type
                existing_annotation_graphics.setVisible(self.annotation_display_checkboxes[annotation_type].isChecked())

    def restore_annotations(self):
        for annotation in self.visualisation_master.sim_data.annotation_data:
            self._add_annotation_graphics(annotation)

        view_rect = QtCore.QRectF(0.0, 0.0, self.ui.annotationGraphicsView.scene().itemsBoundingRect().width(), 1.0)
        self.ui.annotationGraphicsView.fitInView(view_rect, QtCore.Qt.KeepAspectRatio)

    def stop_annotation(self):
        if self.annotating_active:
            if self.visualisation_master.frame_number > self.current_new_annotation.first_frame:
                self.current_new_annotation.last_frame = self.visualisation_master.frame_number
                self.current_new_annotation.notes = self.ui.annotationNoteLineEdit.text()
                self.current_new_annotation.ego_vehicle_id = self.ui.annotationEgoCarComboBox.currentData()

                self.visualisation_master.save_annotation(self.current_new_annotation)
                self._add_annotation_graphics(self.current_new_annotation)

                self.current_new_annotation = None
                self.annotating_active = False
                self.ui.annotationNoteLineEdit.setText("")
            else:
                print('cannot end an annotation before it starts')

    def start_annotation(self):
        self.annotating_active = True
        self.current_new_annotation = Annotation(self.visualisation_master.sim_data.dataset_id)
        self.current_new_annotation.first_frame = self.visualisation_master.frame_number
        self._update_annotation_info()

    def _add_annotation_graphics(self, annotation):
        annotation_graphics = AnnotationGraphicsObject(annotation, self.visualisation_master.total_number_of_frames, self)
        x_position = round(1000 * annotation.first_frame / self.visualisation_master.total_number_of_frames)
        y_position = 6.0
        success = False
        # increment y position of annotation until no overlap with other existing annotations exists
        while not success:
            y_position -= 6.0
            overlap_found = False
            for existing_annotation_graphics in self.ui.annotationGraphicsView.items():
                if isinstance(existing_annotation_graphics, AnnotationGraphicsObject):
                    if existing_annotation_graphics.pos().y() == y_position:
                        if existing_annotation_graphics.annotation.first_frame <= annotation.last_frame + 50:
                            if existing_annotation_graphics.annotation.last_frame >= annotation.first_frame - 50:
                                overlap_found = True
                                break
            success = not overlap_found

        annotation_graphics.setPos(x_position, y_position)
        self.ui.annotationGraphicsView.scene().addItem(annotation_graphics)

    def select_annotation(self, annotation_graphics):
        if self.current_new_annotation:
            return
        if self.selected_annotation_graphics is annotation_graphics:
            annotation_graphics.set_highlight(False)
            self.selected_annotation_graphics = None
            self.selected_annotation = None
            self.selected_invisible_vehicle_id = None
        else:
            if self.selected_annotation_graphics:
                self.selected_annotation_graphics.set_highlight(False)
            annotation_graphics.set_highlight(True)
            self.selected_annotation_graphics = annotation_graphics
            self.selected_annotation = annotation_graphics.annotation
            if annotation_graphics.annotation.ego_vehicle_id in self.vehicles.keys():
                self.select_vehicle(self.vehicles[annotation_graphics.annotation.ego_vehicle_id])
            else:
                self.selected_invisible_vehicle_id = annotation_graphics.annotation.ego_vehicle_id
        self._update_annotation_info()

    def toggle_play(self, record=False):
        if self.overlay_visible:
            self._toggle_overlay()
        if self.visualisation_master:
            self.visualisation_master.toggle_running(record=record)
            self.update_buttons()

    def fast_forward(self):
        if self.overlay_visible:
            self._toggle_overlay()
        if self.visualisation_master:
            self.visualisation_master.fast_forward()
            self.update_buttons()

    def reverse(self):
        if self.overlay_visible:
            self._toggle_overlay()
        if self.visualisation_master:
            self.visualisation_master.reverse()
            self.update_buttons()

    def step_frame(self, step_size):
        if self.overlay_visible:
            self._toggle_overlay()
        if self.visualisation_master:
            self.visualisation_master.step_frame(step_size)

    def add_vehicle(self, vehicle, vehicle_id):
        self.vehicles[vehicle_id] = vehicle
        self.view.add_vehicle(vehicle, vehicle_id)

        if self.selected_invisible_vehicle_id == vehicle.id:
            self.select_vehicle(vehicle)

    def remove_vehicle(self, vehicle, vehicle_id):
        if self.selected_vehicle is vehicle:
            self.view.deselect_vehicle(self.selected_vehicle)
            self.selected_vehicle = None
            self.vehicle_info_widget.clear_info_fields()
            self.vehicle_info_widget.enable_all_fields(False)

        self.view.remove_vehicle(vehicle_id)
        self.vehicles.pop(vehicle_id)
        self.ui.annotationEgoCarComboBox.removeItem(self.ui.annotationEgoCarComboBox.findData(vehicle.id))

    def select_vehicle(self, vehicle):
        if self.selected_vehicle is vehicle:
            self.view.deselect_vehicle(self.selected_vehicle)
            self.selected_vehicle = None
            self.vehicle_info_widget.clear_info_fields()
            self.vehicle_info_widget.enable_all_fields(False)
        else:
            if self.selected_vehicle:
                self.view.deselect_vehicle(self.selected_vehicle)
            self.view.select_vehicle(vehicle)
            self.selected_vehicle = vehicle
            self.vehicle_info_widget.update_information(vehicle)
            self.vehicle_info_widget.enable_all_fields(True)
            if not self.annotating_active:
                self.ui.annotationEgoCarComboBox.setCurrentText(str(vehicle.id))

    def get_image_of_current_view(self):
        original_map_size = self.view.map_item.pixmap().size()

        if self.dataset_id.data_source in [DataSource.NGSIM, DataSource.PNEUMA]:
            # NGSIM and PNeuma Maps are quite big, scale them down and save at 25%
            original_map_size = 0.25 * original_map_size

        scene_bounding_rect = self.view.map_item.sceneBoundingRect()

        image = QtGui.QImage(original_map_size, QtGui.QImage.Format_ARGB32_Premultiplied)
        image_rect = QtCore.QRectF(image.rect())

        painter = QtGui.QPainter(image)
        self.view.scene.render(painter, image_rect, scene_bounding_rect, QtCore.Qt.KeepAspectRatio)
        painter.end()

        return image

    def save_current_scene(self):
        save_path, _ = QtWidgets.QFileDialog.getSaveFileName(self, 'Save current scene', 'data', filter='*.png')

        if save_path:
            self.get_image_of_current_view().save(save_path)

    def _update_annotation_info(self):
        self._set_annotation_save_signals_blocked(True)
        self.ui.startAnnotationPushButton.setEnabled(not bool(self.selected_annotation) and not bool(self.current_new_annotation))
        self.ui.stopAnnotationPushButton.setEnabled(not bool(self.selected_annotation) and bool(self.current_new_annotation))
        self.ui.createPlotsPushButton.setEnabled(
            isinstance(self.visualisation_master, HighDVisualisationMaster) and bool(self.selected_annotation) and not bool(self.current_new_annotation))

        if self.selected_annotation:
            self.ui.annotationNoteLineEdit.setText(self.selected_annotation.notes)
            self.ui.annotationEgoCarComboBox.setCurrentText(str(self.selected_annotation.ego_vehicle_id))
            self.ui.annotationFirstFrameSpinBox.setValue(self.selected_annotation.first_frame)
            self.ui.annotationLastFrameSpinBox.setValue(self.selected_annotation.last_frame)
        if self.current_new_annotation:
            self.ui.annotationNoteLineEdit.setText(self.current_new_annotation.notes)
            self.ui.annotationEgoCarComboBox.setCurrentText(str(self.current_new_annotation.ego_vehicle_id))
            self.ui.annotationFirstFrameSpinBox.setValue(self.current_new_annotation.first_frame)
            self.ui.annotationLastFrameSpinBox.setValue(self.current_new_annotation.last_frame)
        elif not self.selected_annotation and not self.current_new_annotation:
            self.ui.annotationNoteLineEdit.setText('')
        self._set_annotation_save_signals_blocked(False)

    def _set_annotation_save_signals_blocked(self, blocked):
        self.ui.annotationLastFrameSpinBox.blockSignals(blocked)
        self.ui.annotationFirstFrameSpinBox.blockSignals(blocked)
        self.ui.annotationNoteLineEdit.blockSignals(blocked)
        self.ui.annotationEgoCarComboBox.blockSignals(blocked)

    def _save_annotation_changes(self):
        if self.selected_annotation and not self.current_new_annotation:
            self.selected_annotation.first_frame = self.ui.annotationFirstFrameSpinBox.value()
            self.selected_annotation.last_frame = self.ui.annotationLastFrameSpinBox.value()
            self.selected_annotation.notes = self.ui.annotationNoteLineEdit.text()
            self.selected_annotation.ego_vehicle_id = self.ui.annotationEgoCarComboBox.currentData()
            self.selected_annotation_graphics.update_borders()

    def update_all_graphics_positions(self):
        self.view.update_all_graphics_positions()
        if self.selected_vehicle:
            self.vehicle_info_widget.update_information(self.selected_vehicle)

    def update_time_in_gui(self, time: datetime.datetime, frame_number):
        if self.end_time:
            self.ui.timeSlider.setValue((time - self.start_time) * 1000 / (self.end_time - self.start_time))

        self.ui.frameSpinBox.setValue(frame_number)
        self.ui.timeEdit.setTime(time.time())

    def update_buttons(self):
        if self.visualisation_master:
            if self.visualisation_master.is_running:
                self.ui.playButton.setText('Pause')
            else:
                self.ui.playButton.setText('Play')

        self.ui.nextFramePushButton.setEnabled(bool(self.visualisation_master) and not self.visualisation_master.is_running)
        self.ui.previousFramePushButton.setEnabled(bool(self.visualisation_master) and not self.visualisation_master.is_running)
        self.ui.playButton.setEnabled(bool(self.visualisation_master))
        self.ui.recordPushButton.setEnabled(bool(self.visualisation_master) and not self.visualisation_master.is_running)
        self.ui.fastForwardButton.setEnabled(bool(self.visualisation_master))
        self.ui.rewindButton.setEnabled(bool(self.visualisation_master))
        self.ui.timeEdit.setEnabled(bool(self.visualisation_master))
        self.ui.createOverlayPushButton.setEnabled(
            bool(self.visualisation_master) and isinstance(self.visualisation_master, HighDVisualisationMaster) and not self.visualisation_master.is_running)

    def set_time(self, value):
        if self.overlay_visible:
            self._toggle_overlay()
        if self.visualisation_master:
            self.visualisation_master.set_time(value / 1000)

    def _create_plots(self):
        """
        This is an example of plots that can be made. It plots a number of things based on an annotation.
        This example only works with HighD data.
        """
        track_data = self.visualisation_master.sim_data.track_data
        meta_data = self.visualisation_master.sim_data.track_meta_data
        ego_vehicle_id = self.selected_annotation.ego_vehicle_id

        data_in_annotation = track_data.loc[
                             (self.selected_annotation.first_frame <= track_data.frame) & (track_data.frame <= self.selected_annotation.last_frame), :]
        vehicles_driving_in_the_same_direction = meta_data.loc[meta_data.drivingDirection == meta_data.at[ego_vehicle_id, 'drivingDirection']].index

        ego_vehicle_x = data_in_annotation.loc[track_data.id == self.selected_annotation.ego_vehicle_id, 'x'].to_numpy()
        ego_vehicle_y = data_in_annotation.loc[track_data.id == self.selected_annotation.ego_vehicle_id, 'y'].to_numpy()

        tracks_plot = pyqtgraph.PlotWindow(title='Tracks')
        tracks_plot.plot(ego_vehicle_x, ego_vehicle_y, pen='r', width=3)
        tracks_plot.setLabel('left', 'y [m]')
        tracks_plot.setLabel('bottom', 'x [m]')

        self.plot_dialogs.append(tracks_plot)

        interesting_vehicles = data_in_annotation.loc[data_in_annotation.id.isin(vehicles_driving_in_the_same_direction), :]

        for other_vehicle_id in interesting_vehicles.id.unique():
            vehicle_x = data_in_annotation.loc[data_in_annotation.id == other_vehicle_id, 'x'].to_numpy()
            vehicle_y = data_in_annotation.loc[data_in_annotation.id == other_vehicle_id, 'y'].to_numpy()
            tracks_plot.plot(vehicle_x, vehicle_y, pen='w', width=1)

        ego_vehicle_acceleration = data_in_annotation.loc[track_data.id == self.selected_annotation.ego_vehicle_id, 'xAcceleration'].to_numpy()
        ego_vehicle_ttc = data_in_annotation.loc[track_data.id == self.selected_annotation.ego_vehicle_id, 'ttc'].to_numpy()
        ego_vehicle_thw = data_in_annotation.loc[track_data.id == self.selected_annotation.ego_vehicle_id, 'thw'].to_numpy()
        ego_vehicle_dhw = data_in_annotation.loc[track_data.id == self.selected_annotation.ego_vehicle_id, 'dhw'].to_numpy()
        velocity_difference = data_in_annotation.loc[track_data.id == self.selected_annotation.ego_vehicle_id, 'xVelocity'].to_numpy() - data_in_annotation.loc[
            track_data.id == self.selected_annotation.ego_vehicle_id, 'precedingXVelocity'].to_numpy()
        ego_vehicle_y_velocity = data_in_annotation.loc[track_data.id == self.selected_annotation.ego_vehicle_id, 'yVelocity'].to_numpy()

        pyqtgraph.plot(ego_vehicle_acceleration,
                       title='Acceleration, Vehicle: %d, Dataset: %d' % (ego_vehicle_id, self.visualisation_master.sim_data.recording_id),
                       left='x Acceleration [m/s^2]',
                       bottom='frames')
        pyqtgraph.plot(ego_vehicle_dhw,
                       title='DHW, Vehicle: %d, Dataset: %d' % (ego_vehicle_id, self.visualisation_master.sim_data.recording_id),
                       left='DHW [m]',
                       bottom='frames'
                       )
        pyqtgraph.plot(ego_vehicle_thw,
                       title='THW, Vehicle: %d, Dataset: %d' % (ego_vehicle_id, self.visualisation_master.sim_data.recording_id),
                       left='THW [s]',
                       bottom='frames'
                       )
        pyqtgraph.plot(ego_vehicle_ttc,
                       title='TTC, Vehicle: %d, Dataset: %d' % (ego_vehicle_id, self.visualisation_master.sim_data.recording_id),
                       left='TTC [s]',
                       bottom='frames'
                       )
        pyqtgraph.plot(velocity_difference,
                       title='Velocity difference, Vehicle: %d, Dataset: %d' % (ego_vehicle_id, self.visualisation_master.sim_data.recording_id),
                       left='delta v [m/s]',
                       bottom='frames'
                       )

        y_vel_plot = pyqtgraph.PlotWindow(title='Y Velocity, Vehicle: %d, Dataset: %d' % (ego_vehicle_id, self.visualisation_master.sim_data.recording_id))
        y_vel_plot.addLegend()
        y_vel_plot.setLabel('left', 'y velocity [m/s]')
        y_vel_plot.setLabel('bottom', 'Frames since first appearance')

        y_vel_plot.plot(ego_vehicle_y_velocity, name='Y velocity')
        y_vel_plot.plot([np.mean(ego_vehicle_y_velocity)] * len(ego_vehicle_y_velocity), pen=pyqtgraph.mkPen('r', style=QtCore.Qt.DashLine),
                        name='Mean Y velocity')
        y_vel_plot.plot([np.mean(ego_vehicle_y_velocity) / 2] * len(ego_vehicle_y_velocity), pen='r', name='Half Mean Y velocity')
        self.plot_dialogs.append(y_vel_plot)

    def _toggle_overlay(self):
        """
        This is an example of how to create a heatmap overlay. The reward function used here purely serves as an example and has no meaning.
        This example only works with HighD datasets
        """
        if self.overlay_visible:
            self.view.remove_overlay()
            self.overlay_visible = False
        elif isinstance(self.visualisation_master.sim_data, HighDDataset):
            self.setCursor(QtCore.Qt.WaitCursor)

            surrounding_vehicles_positions = []
            for id, vehicle in self.vehicles.items():
                surrounding_vehicles_positions.append(vehicle.center_position)

            surrounding_vehicles_positions = np.array(surrounding_vehicles_positions)

            pixels_per_meter = 5
            map_width = self.view.map_item.sceneBoundingRect().width()
            map_height = self.view.map_item.sceneBoundingRect().height()
            pixel_width = round(map_width * pixels_per_meter)
            pixel_height = round(map_height * pixels_per_meter)

            lane_centers = []

            upper_markings = self.visualisation_master.sim_data.upper_lane_markings
            lower_markings = self.visualisation_master.sim_data.lower_lane_markings

            for index in range(len(upper_markings) - 1):
                lane_centers.append((upper_markings[index + 1] - upper_markings[index]) / 2 + upper_markings[index])

            for index in range(len(lower_markings) - 1):
                lane_centers.append((lower_markings[index + 1] - lower_markings[index]) / 2 + lower_markings[index])

            x = [np.array([w / pixels_per_meter, h / pixels_per_meter]) for h in range(pixel_height) for w in range(pixel_width)]
            args = zip(x, [surrounding_vehicles_positions] * len(x), [lane_centers] * len(x))

            with multiprocessing.Pool(10) as p:
                costs_per_position = p.starmap(cost_function, args)

            overlay_data = np.array(costs_per_position)
            overlay_data.resize((pixel_height, pixel_width))

            self.view.add_overlay(overlay_data, pixel_width, pixel_height)
            self.overlay_visible = True
            self.update_buttons()
            self.setCursor(QtCore.Qt.ArrowCursor)

    def resizeEvent(self, e):
        view_rect = QtCore.QRectF(0.0, 0.0, self.ui.annotationGraphicsView.scene().itemsBoundingRect().width(), 1.0)
        self.ui.annotationGraphicsView.fitInView(view_rect, QtCore.Qt.KeepAspectRatio)
        super().resizeEvent(e)
