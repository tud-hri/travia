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
import math

import numpy as np
from PyQt5 import QtWidgets, QtGui, QtCore
from dataobjects.enums import DataSource

from .vehiclegraphics import VehicleGraphicsObject
from .overlay import Overlay

METERS_PER_US_SURVEY_FOOT = 0.3048006096


class WorldView(QtWidgets.QGraphicsView):
    def __init__(self, main_gui, dataset_id, parent=None):
        super().__init__(parent)

        self.main_gui = main_gui
        self.scene = QtWidgets.QGraphicsScene()
        self.setRenderHint(QtGui.QPainter.HighQualityAntialiasing)
        self.setScene(self.scene)
        self.setBackgroundBrush(QtGui.QBrush(QtGui.QColor(186, 186, 186)))

        self.map_item = None
        self.overlay_item = None
        self._load_background(dataset_id)

        self.dial = QtWidgets.QDial(parent=self)
        self.dial.setFixedHeight(50)
        self.dial.setFixedWidth(50)
        self.dial.setWrapping(True)
        self.dial.setRange(-180, 180)
        self.dial.valueChanged.connect(self._update_rotation)
        self.current_rotation = 0.

        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)

        padding_rect_size = self.map_item.sceneBoundingRect().size() * 2.0
        padding_rect_top_left_x = self.map_item.sceneBoundingRect().center().x() - padding_rect_size.width() / 2
        padding_rect_top_left_y = self.map_item.sceneBoundingRect().center().y() - padding_rect_size.height() / 2
        scroll_padding_rect = QtWidgets.QGraphicsRectItem(padding_rect_top_left_x, padding_rect_top_left_y, padding_rect_size.width(),
                                                          padding_rect_size.height())
        scroll_padding_rect.setPen(QtGui.QPen(QtCore.Qt.NoPen))
        self.scene.addItem(scroll_padding_rect)

        # Scaled size zoomRect
        self.max_zoom_size = self.map_item.sceneBoundingRect().size() * 1
        self.min_zoom_size = self.map_item.sceneBoundingRect().size() * 0.01
        self.zoom_level = 0.0
        self.zoom_center = self.map_item.sceneBoundingRect().center()
        self.update_zoom()

        self.graphics_objects = {}

    def _load_background(self, dataset_id):
        if dataset_id.data_source is DataSource.HIGHD:
            meters_per_pixel = 4 * 0.10106  # from MATLAB example code

            pixmap = QtGui.QPixmap('data/' + dataset_id.map_sub_folder + dataset_id.map_image_name + '.png')
            actual_height = pixmap.height() * meters_per_pixel
            self.map_item = QtWidgets.QGraphicsPixmapItem(pixmap)
            scale_factor = self.map_item.sceneBoundingRect().height()/actual_height
            self.map_item.setScale(meters_per_pixel)

            self.map_item.setPos(0, 0)
            self.scene.addItem(self.map_item)
        elif dataset_id.data_source in [DataSource.NGSIM, DataSource.PNEUMA]:
            path_to_file = 'data/' + dataset_id.map_sub_folder + dataset_id.map_image_name
            pixmap = QtGui.QPixmap(path_to_file + '.tif')
            self.map_item = QtWidgets.QGraphicsPixmapItem(pixmap)

            with open(path_to_file + '.tfw', 'r') as map_info_file:
                horizontal_resolution = float(map_info_file.readline())
                rotation_1 = float(map_info_file.readline())
                rotation_2 = float(map_info_file.readline())
                vertical_resolution = float(map_info_file.readline())
                bottom_left_x = float(map_info_file.readline())
                bottom_left_y = float(map_info_file.readline())

            if dataset_id.data_source is DataSource.NGSIM:
                horizontal_resolution *= METERS_PER_US_SURVEY_FOOT
                vertical_resolution *= METERS_PER_US_SURVEY_FOOT
                bottom_left_x *= METERS_PER_US_SURVEY_FOOT
                bottom_left_y *= METERS_PER_US_SURVEY_FOOT

            if rotation_1 or rotation_2:
                raise ValueError('The loaded tif/tfw map is rotated, the traffic visualiser is currently not able to handle this.')

            vertical_resolution = abs(vertical_resolution)

            transform = QtGui.QTransform.fromScale(horizontal_resolution, vertical_resolution)
            self.map_item.setTransform(transform)
            self.map_item.setPos(bottom_left_x, - bottom_left_y)
            self.scene.addItem(self.map_item)

    def add_vehicle(self, vehicle_object, vehicle_id):
        vehicle_graphics = VehicleGraphicsObject(vehicle_object, self.main_gui, vehicle_id)

        self.scene.addItem(vehicle_graphics)

        self.graphics_objects[vehicle_id] = vehicle_graphics
        self.update_all_graphics_positions()

    def remove_vehicle(self, vehicle_id):
        graphics_item = self.graphics_objects.pop(vehicle_id)
        self.scene.removeItem(graphics_item)
        graphics_item.parent = None
        self.update_all_graphics_positions()

    def select_vehicle(self, vehicle_object):
        try:
            self.graphics_objects[str(vehicle_object.id)].set_highlight(True)
        except KeyError:  # a car is selected that is not present in the current frame
            pass

    def deselect_vehicle(self, vehicle_object):
        try:
            self.graphics_objects[str(vehicle_object.id)].set_highlight(False)
        except KeyError:  # a car is deselected that is not present in the current frame
            pass

    def update_all_graphics_positions(self):
        for _, graphics_object in self.graphics_objects.items():
            if any(graphics_object.vehicle.current_position):
                graphics_object.setPos(graphics_object.vehicle.current_position[0], graphics_object.vehicle.current_position[1])
                graphics_object.setRotation(-np.degrees(graphics_object.vehicle.current_heading))

    def update_zoom(self):
        # Compute scale factors (in x- and y-direction)
        zoom = (1.0 - self.zoom_level) ** 2
        scale1 = zoom + (self.min_zoom_size.width() / self.max_zoom_size.width()) * (1.0 - zoom)
        scale2 = zoom + (self.min_zoom_size.height() / self.max_zoom_size.height()) * (1.0 - zoom)

        # Scaled size zoomRect
        scaled_w = self.max_zoom_size.width() * scale1
        scaled_h = self.max_zoom_size.height() * scale2

        # Set zoomRect
        view_zoom_rect = QtCore.QRectF(self.zoom_center.x() - scaled_w / 2, self.zoom_center.y() - scaled_h / 2, scaled_w, scaled_h)
        # Set view
        self.fitInView(view_zoom_rect, QtCore.Qt.KeepAspectRatio)

    def add_overlay(self, data, width, height):
        overlay_pixmap = Overlay(data, width, height)

        self.overlay_item = QtWidgets.QGraphicsPixmapItem(overlay_pixmap)
        self.overlay_item.setScale(self.map_item.sceneBoundingRect().width() / width)
        self.overlay_item.setOpacity(0.5)
        self.scene.addItem(self.overlay_item)

    def remove_overlay(self):
        self.scene.removeItem(self.overlay_item)
        self.overlay_item = None

    def _update_rotation(self):
        new_rotation = self.dial.value()
        self.rotate(new_rotation - self.current_rotation)
        self.current_rotation = new_rotation

    def resizeEvent(self, e):
        super().resizeEvent(e)
        self.update_zoom()

    def wheelEvent(self, event):
        direction = np.sign(event.angleDelta().y())
        self.zoom_level = max(min(self.zoom_level + direction * 0.1, 1.0), 0.0)
        self.update_zoom()

    def enterEvent(self, e):
        self.viewport().setCursor(QtCore.Qt.ArrowCursor)
        super().enterEvent(e)

    def mouseMoveEvent(self, e):
        if e.buttons() == QtCore.Qt.LeftButton:  # Drag scene
            self.zoom_center = self.mapToScene(self.rect().center())
        super().mouseMoveEvent(e)

    def mousePressEvent(self, e):
        if e.buttons() == QtCore.Qt.MiddleButton:  # Drag scene
            print('position of mouse: %0.1f, %0.1f ' % (self.mapToScene(e.pos()).x(), self.mapToScene(e.pos()).y()))
        super().mousePressEvent(e)

    def mouseReleaseEvent(self, e):
        super().mouseReleaseEvent(e)
        self.viewport().setCursor(QtCore.Qt.ArrowCursor)
        self.update_zoom()
