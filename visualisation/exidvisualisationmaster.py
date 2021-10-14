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
import numpy as np

from dataobjects import ExiDDataset, Vehicle
from .visualisationmaster import VisualisationMaster


class ExiDVisualisationMaster(VisualisationMaster):
    sim_data: ExiDDataset

    def __init__(self, sim_data, gui, start_time, end_time, number_of_frames, first_frame, dt, parent=None):
        super().__init__(sim_data, gui, start_time, end_time, number_of_frames, first_frame, dt, parent=parent)

    def do_time_step(self):

        data_on_timestamp = self.sim_data.track_data.loc[self.sim_data.track_data.frame == self.frame_number, :]

        for item in data_on_timestamp.index:
            vehicle_id = data_on_timestamp.at[item, 'trackId']
            global_x = data_on_timestamp.at[item, 'xCenter']
            global_y = data_on_timestamp.at[item, 'yCenter']
            heading = data_on_timestamp.at[item, 'heading']
            velocity_x = data_on_timestamp.at[item, 'xVelocity']
            velocity_y = data_on_timestamp.at[item, 'yVelocity']
            acceleration_x = data_on_timestamp.at[item, 'xAcceleration']
            acceleration_y = data_on_timestamp.at[item, 'yAcceleration']

            lon_velocity = data_on_timestamp.at[item, 'lonVelocity']
            lat_velocity = data_on_timestamp.at[item, 'latVelocity']
            lon_acceleration = data_on_timestamp.at[item, 'lonAcceleration']
            lat_acceleration = data_on_timestamp.at[item, 'latAcceleration']

            if str(vehicle_id) not in self.vehicles.keys():
                new_vehicle = Vehicle.from_exid_row(self.sim_data.track_meta_data.loc[self.sim_data.track_meta_data.index == vehicle_id, :])
                self._add_vehicle(new_vehicle, str(vehicle_id))

            self.vehicles[str(vehicle_id)].set_pos_from_center_position(np.array([global_x, global_y]), heading)
            self.vehicles[str(vehicle_id)].current_heading = heading
            self.vehicles[str(vehicle_id)].current_linear_velocities[0] = velocity_x
            self.vehicles[str(vehicle_id)].current_linear_velocities[1] = velocity_y
            self.vehicles[str(vehicle_id)].current_linear_accelerations[0] = acceleration_x
            self.vehicles[str(vehicle_id)].current_linear_accelerations[1] = acceleration_y

            self.vehicles[str(vehicle_id)].current_lon_acceleration = lon_acceleration
            self.vehicles[str(vehicle_id)].current_lat_acceleration = lat_acceleration
            self.vehicles[str(vehicle_id)].current_lon_velocity = lon_velocity
            self.vehicles[str(vehicle_id)].current_lat_velocity = lat_velocity

        self._remove_vehicles_that_are_out_of_frame()
        self.gui.update_time_in_gui(self.t, self.frame_number)
        self.gui.update_all_graphics_positions()

    def get_all_vehicle_ids(self):
        return self.sim_data.track_meta_data.index.to_numpy()
