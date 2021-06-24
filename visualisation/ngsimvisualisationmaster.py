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

from dataobjects import NGSimDataset, Vehicle
from .visualisationmaster import VisualisationMaster


class NGSimVisualisationMaster(VisualisationMaster):
    sim_data: NGSimDataset

    def __init__(self, sim_data, gui, start_time, end_time, number_of_frames, first_frame, parent=None):
        super().__init__(sim_data, gui, start_time, end_time, number_of_frames, first_frame, dt=datetime.timedelta(milliseconds=100), parent=parent)

    def do_time_step(self):

        data_on_timestamp = self.sim_data.track_data.loc[self.sim_data.track_data['Global_Time'] == self.t.timestamp() * 1000, :]

        for index in data_on_timestamp.index:
            vehicle_id = data_on_timestamp.at[index, 'Vehicle_ID']
            if str(vehicle_id) not in self.vehicles.keys():
                first_frame = self.sim_data.track_data.loc[self.sim_data.track_data['Vehicle_ID'] == vehicle_id, 'Frame_ID'].min()
                last_frame = self.sim_data.track_data.loc[self.sim_data.track_data['Vehicle_ID'] == vehicle_id, 'Frame_ID'].max()
                smoothing_succeeded = not self.sim_data.track_data.loc[self.sim_data.track_data['Vehicle_ID'] == vehicle_id, 'Smoothed_Global_X'].isnull().all()
                vehicle = Vehicle.from_ngsim_row(data_on_timestamp.loc[index, :], first_frame, last_frame, smoothing_succeeded)
                self._add_vehicle(vehicle, str(vehicle.id))

            if not self.vehicles[str(vehicle_id)].smoothing_succeeded:
                self.vehicles[str(vehicle_id)].current_position[0] = data_on_timestamp.at[index, 'Global_X']
                self.vehicles[str(vehicle_id)].current_position[1] = - data_on_timestamp.at[index, 'Global_Y']
                self.vehicles[str(vehicle_id)].current_forward_velocity = data_on_timestamp.at[index, 'v_Vel']
            else:
                self.vehicles[str(vehicle_id)].current_position[0] = data_on_timestamp.at[index, 'Smoothed_Global_X']
                self.vehicles[str(vehicle_id)].current_position[1] = - data_on_timestamp.at[index, 'Smoothed_Global_Y']
                self.vehicles[str(vehicle_id)].current_forward_velocity = data_on_timestamp.at[index, 'Smoothed_Vel']
                self.vehicles[str(vehicle_id)].current_heading = data_on_timestamp.at[index, 'Smoothed_Heading']

            self.vehicles[str(vehicle_id)].current_forwards_acceleration = data_on_timestamp.at[index, 'v_Acc']
            self.vehicles[str(vehicle_id)].last_time_stamp = data_on_timestamp.at[index, 'Global_Time']
            self.vehicles[str(vehicle_id)].dhw = data_on_timestamp.at[index, 'Space_Headway']
            self.vehicles[str(vehicle_id)].thw = data_on_timestamp.at[index, 'Time_Headway']
            try:
                self.vehicles[str(vehicle_id)].driving_direction = data_on_timestamp.at[index, 'Direction']
            except KeyError:
                pass

            self.vehicles[str(vehicle_id)].current_lane = data_on_timestamp.at[index, 'Lane_ID']
            self.vehicles[str(vehicle_id)].preceding_id = data_on_timestamp.at[index, 'Preceding']
            self.vehicles[str(vehicle_id)].following_id = data_on_timestamp.at[index, 'Following']
            try:
                self.vehicles[str(vehicle_id)].movement = data_on_timestamp.at[index, 'Movement']
            except KeyError:
                pass

            try:
                self.vehicles[str(vehicle_id)].intersection = data_on_timestamp.at[index, 'Int_ID']
            except KeyError:
                pass

            try:
                self.vehicles[str(vehicle_id)].section = data_on_timestamp.at[index, 'Section_ID']
            except KeyError:
                pass

            try:
                self.vehicles[str(vehicle_id)].origin_zone = data_on_timestamp.at[index, 'O_Zone']
            except KeyError:
                pass

            try:
                self.vehicles[str(vehicle_id)].destination_zone = data_on_timestamp.at[index, 'D_Zone']
            except KeyError:
                pass

        self._remove_vehicles_that_are_out_of_frame()
        self.gui.update_all_graphics_positions()
        self.gui.update_time_in_gui(self.t, self.frame_number)

    def get_all_vehicle_ids(self):
        return self.sim_data.track_data['Vehicle_ID'].unique()
