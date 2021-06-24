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
from dataobjects import PNeumaDataset, Vehicle
from .visualisationmaster import VisualisationMaster


class PNeumaVisualisationMaster(VisualisationMaster):
    sim_data: PNeumaDataset

    def __init__(self, sim_data, gui, start_time, end_time, number_of_frames, first_frame, dt, default_frame_step, parent=None):
        super().__init__(sim_data, gui, start_time, end_time, number_of_frames, first_frame, dt, default_frame_step, parent=parent)

    def do_time_step(self):

        sim_time = (self.t - self.sim_data.start_time).total_seconds()
        data_on_timestamp = self.sim_data.track_data.loc[self.sim_data.track_data.time == sim_time, :]

        for item in data_on_timestamp.index:
            vehicle_id = int(data_on_timestamp.at[item, 'vehicle_id'])

            if str(vehicle_id) not in self.vehicles.keys():
                time_stamps = self.sim_data.track_data.loc[self.sim_data.track_data['vehicle_id'] == vehicle_id, 'time']

                first_frame = int(time_stamps.min() * self.sim_data.frame_rate)
                last_frame = int(time_stamps.max() * self.sim_data.frame_rate)
                smoothing_succeeded = not self.sim_data.track_data.loc[self.sim_data.track_data['vehicle_id'] == vehicle_id, 'smoothed_global_x'].isnull().all()
                data_row = self.sim_data.vehicles.loc[self.sim_data.vehicles['track_id'] == vehicle_id, :]
                new_vehicle = Vehicle.from_pneuma_row(data_row, first_frame, last_frame, smoothing_succeeded)
                self._add_vehicle(new_vehicle, str(vehicle_id))

            if self.vehicles[str(vehicle_id)].smoothing_succeeded:
                self.vehicles[str(vehicle_id)].current_position[0] = data_on_timestamp.at[item, 'smoothed_global_x']
                self.vehicles[str(vehicle_id)].current_position[1] = - data_on_timestamp.at[item, 'smoothed_global_y']
                self.vehicles[str(vehicle_id)].current_forward_velocity = data_on_timestamp.at[item, 'smoothed_speed']
                self.vehicles[str(vehicle_id)].current_heading = data_on_timestamp.at[item, 'smoothed_heading']
            else:
                self.vehicles[str(vehicle_id)].current_position[0] = data_on_timestamp.at[item, 'global_x']
                self.vehicles[str(vehicle_id)].current_position[1] = - data_on_timestamp.at[item, 'global_y']
                self.vehicles[str(vehicle_id)].current_forward_velocity = data_on_timestamp.at[item, 'speed']

            self.vehicles[str(vehicle_id)].current_lon_acceleration = data_on_timestamp.at[item, 'lon_acc']
            self.vehicles[str(vehicle_id)].current_lat_acceleration = data_on_timestamp.at[item, 'lat_acc']
            self.vehicles[str(vehicle_id)].last_time_stamp = data_on_timestamp.at[item, 'time']

        self._remove_vehicles_that_are_out_of_frame()
        self.gui.update_all_graphics_positions()
        self.gui.update_time_in_gui(self.t, self.frame_number)

    def get_all_vehicle_ids(self):
        return self.sim_data.track_data['vehicle_id'].unique()
