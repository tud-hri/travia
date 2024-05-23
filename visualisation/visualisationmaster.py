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
import os
import cv2

import numpy as np

from PyQt5 import QtCore, QtWidgets, QtGui

from dataobjects import Vehicle


class VisualisationMaster(QtCore.QObject):
    FAST_FORWARD_FACTOR = 4
    video_writer: cv2.VideoWriter

    def __init__(self, sim_data, gui, start_time, end_time, number_of_frames, first_frame, dt, default_frame_step=1, parent=None):
        super().__init__(parent)

        self.dt = dt
        self.default_frame_step = default_frame_step
        self.is_running_fast_forward = False
        self.is_running_reverse = False
        self.is_recording = False

        self.video_writer = None
        self.path_to_video_file = ''

        self.main_timer = QtCore.QTimer()
        self.main_timer.setInterval(int(self.dt.total_seconds() * 1e3))
        self.main_timer.setTimerType(QtCore.Qt.PreciseTimer)
        self.main_timer.setSingleShot(False)
        self.main_timer.timeout.connect(self._do_time_step_wrapper)

        self.start_time = start_time
        self.end_time = end_time
        self.total_number_of_frames = number_of_frames
        self.first_frame = first_frame - 1
        self.frame_number = self.first_frame
        self.t = self.start_time - self.dt

        self.gui = gui
        self.sim_data = sim_data
        self.vehicles = {}

        self._do_time_step_wrapper()

    def start(self):
        self.main_timer.start()

    def set_time(self, per_mille_of_frames):
        self.frame_number = round(per_mille_of_frames * self.total_number_of_frames + self.first_frame)
        self.t = self.start_time + datetime.timedelta(microseconds=((self.frame_number - self.first_frame) / self.sim_data.frame_rate) * 1e6)
        self._do_time_step_wrapper()

    def step_frame(self, step_size):
        self.frame_number += step_size - 1
        self.t = self.start_time + datetime.timedelta(microseconds=((self.frame_number - self.first_frame) / self.sim_data.frame_rate) * 1e6)
        self._do_time_step_wrapper()

    def toggle_running(self, record=False):
        if self.main_timer.isActive():
            self.main_timer.stop()
            self.main_timer.setInterval(int(self.dt.total_seconds() * 1e3))
            self.is_running_fast_forward = False
            self.is_running_reverse = False
            if self.is_recording:
                self.stop_recording()
        else:
            if record:
                self.initialize_recording()
            self.main_timer.start()
        return self.main_timer.isActive()

    def initialize_recording(self):
        user_video_folder = os.path.join(os.path.expanduser('~'), 'Videos')
        if not os.path.isdir(user_video_folder):
            os.mkdir(user_video_folder)

        file_name = str(self.sim_data.dataset_id) + datetime.datetime.now().strftime('-%Y%m%d-%Hh%Mm%Ss.avi')

        # remove illegal characters from filename
        file_name = file_name.replace(':', '-').replace('/', '-').replace('\\', '-')

        self.path_to_video_file = os.path.join(user_video_folder, file_name)
        fps = self.sim_data.frame_rate

        frame_size = self.gui.get_image_of_current_view().size()
        self.video_writer = cv2.VideoWriter(self.path_to_video_file, cv2.VideoWriter.fourcc('M', 'J', 'P', 'G'), fps, (frame_size.width(), frame_size.height()))
        self.is_recording = True

    def stop_recording(self):
        self.video_writer.release()
        QtWidgets.QMessageBox.information(self.gui, 'Video Saved', 'A video capture of the visualisation was saved to ' + self.path_to_video_file)
        self.is_recording = False

    def _record_frame(self):
        if self.is_recording:
            image = self.gui.get_image_of_current_view()
            frame_size = image.size()
            bits = image.bits()

            bits.setsize(frame_size.height() * frame_size.width() * 4)
            image_array = np.frombuffer(bits, np.uint8).reshape((frame_size.height(), frame_size.width(), 4))
            color_convert_image = cv2.cvtColor(image_array, cv2.COLOR_RGBA2RGB)
            self.video_writer.write(color_convert_image)

    def fast_forward(self):
        return self._fast_run(forward=True)

    def reverse(self):
        return self._fast_run(reverse=True)

    def _fast_run(self, reverse=False, forward=False):
        if self.main_timer.isActive():
            self.main_timer.stop()

        self.main_timer.setInterval(int(self.dt.total_seconds() * 1e3 / self.FAST_FORWARD_FACTOR))
        self.is_running_reverse = reverse
        self.is_running_fast_forward = forward
        self.main_timer.start()

        return self.main_timer.isActive()

    def _add_vehicle(self, vehicle: Vehicle, vehicle_id: str):
        self.vehicles[vehicle_id] = vehicle
        self.gui.add_vehicle(vehicle, vehicle_id)

    def _remove_vehicle(self, vehicle_id):
        self.gui.remove_vehicle(self.vehicles[vehicle_id], vehicle_id)
        del self.vehicles[vehicle_id]

    def _remove_vehicles_that_are_out_of_frame(self):
        list_of_vehicles = list(self.vehicles.keys())
        for vehicle_id in list_of_vehicles:
            if not (self.vehicles[vehicle_id].first_frame <= self.frame_number <= self.vehicles[vehicle_id].last_frame):
                self._remove_vehicle(vehicle_id)

    def _increment_time(self):
        if self.is_running_fast_forward:
            self.frame_number += self.default_frame_step * self.FAST_FORWARD_FACTOR
            self.t += self.FAST_FORWARD_FACTOR * self.dt
        elif self.is_running_reverse:
            self.frame_number -= self.default_frame_step * self.FAST_FORWARD_FACTOR
            self.t -= self.FAST_FORWARD_FACTOR * self.dt
        else:
            self.frame_number += self.default_frame_step
            self.t += self.dt

        if self.t < self.start_time:
            self.t = self.start_time
            self.frame_number = self.first_frame
            if self.main_timer.isActive():
                self.toggle_running()
            self.gui.update_buttons()
        elif self.t >= self.end_time:
            self.t = self.end_time
            self.frame_number = self.first_frame + self.total_number_of_frames
            if self.main_timer.isActive():
                self.toggle_running()
            self.gui.update_buttons()

    def _do_time_step_wrapper(self):
        self._increment_time()
        self.do_time_step()
        self._record_frame()

    def do_time_step(self):
        pass

    def save_annotation(self, annotation):
        self.sim_data.annotation_data.append(annotation)

    def get_all_vehicle_ids(self):
        pass

    @property
    def is_running(self):
        return self.main_timer.isActive()
