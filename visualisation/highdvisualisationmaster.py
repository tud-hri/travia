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

from dataobjects import HighDDataset, Vehicle
from .visualisationmaster import VisualisationMaster


class HighDVisualisationMaster(VisualisationMaster):
    sim_data: HighDDataset

    def __init__(self, sim_data, gui, start_time, end_time, number_of_frames, first_frame, dt, parent=None):
        super().__init__(sim_data, gui, start_time, end_time, number_of_frames, first_frame, dt, parent=parent)

    def do_time_step(self):

        data_on_timestamp = self.sim_data.track_data.loc[self.sim_data.track_data.frame == self.frame_number, :]

        for item in data_on_timestamp.index:
            vehicle_id = int(data_on_timestamp.at[item, 'id'])
            global_x = data_on_timestamp.at[item, 'x']
            global_y = data_on_timestamp.at[item, 'y']
            velocity_x = data_on_timestamp.at[item, 'xVelocity']
            velocity_y = data_on_timestamp.at[item, 'yVelocity']
            acceleration_x = data_on_timestamp.at[item, 'xAcceleration']
            acceleration_y = data_on_timestamp.at[item, 'yAcceleration']
            front_sight = data_on_timestamp.at[item, 'frontSightDistance']
            back_sight = data_on_timestamp.at[item, 'backSightDistance']
            dhw = data_on_timestamp.at[item, 'dhw']
            thw = data_on_timestamp.at[item, 'thw']
            ttc = data_on_timestamp.at[item, 'ttc']
            preceding_x_velocity = data_on_timestamp.at[item, 'precedingXVelocity']
            preceding_id = data_on_timestamp.at[item, 'precedingId']
            following_id = data_on_timestamp.at[item, 'followingId']
            left_preceding_id = data_on_timestamp.at[item, 'leftPrecedingId']
            left_alongside_id = data_on_timestamp.at[item, 'leftAlongsideId']
            left_following_id = data_on_timestamp.at[item, 'leftFollowingId']
            right_preceding_id = data_on_timestamp.at[item, 'rightPrecedingId']
            right_alongside_id = data_on_timestamp.at[item, 'rightAlongsideId']
            right_following_id = data_on_timestamp.at[item, 'rightFollowingId']
            lane_id = data_on_timestamp.at[item, 'laneId']

            if str(vehicle_id) not in self.vehicles.keys():
                new_vehicle = Vehicle.from_highd_row(self.sim_data.track_meta_data.loc[self.sim_data.track_meta_data.index == vehicle_id, :])
                if new_vehicle.driving_direction == 1:  # driving on the top lanes to the left
                    new_vehicle.current_heading = -np.pi
                self._add_vehicle(new_vehicle, str(vehicle_id))

            self.vehicles[str(vehicle_id)].set_pos_from_top_left_corner(np.array([global_x, global_y]))

            self.vehicles[str(vehicle_id)].current_linear_velocities[0] = velocity_x
            self.vehicles[str(vehicle_id)].current_linear_velocities[1] = velocity_y
            self.vehicles[str(vehicle_id)].current_linear_accelerations[0] = acceleration_x
            self.vehicles[str(vehicle_id)].current_linear_accelerations[1] = acceleration_y

            self.vehicles[str(vehicle_id)].front_sight_distance = front_sight
            self.vehicles[str(vehicle_id)].back_sight_distance = back_sight
            self.vehicles[str(vehicle_id)].dhw = dhw
            self.vehicles[str(vehicle_id)].thw = thw
            self.vehicles[str(vehicle_id)].ttc = ttc
            self.vehicles[str(vehicle_id)].preceding_x_velocity = preceding_x_velocity
            self.vehicles[str(vehicle_id)].preceding_id = preceding_id
            self.vehicles[str(vehicle_id)].following_id = following_id
            self.vehicles[str(vehicle_id)].left_preceding_id = left_preceding_id
            self.vehicles[str(vehicle_id)].left_alongside_id = left_alongside_id
            self.vehicles[str(vehicle_id)].left_following_id = left_following_id
            self.vehicles[str(vehicle_id)].right_preceding_id = right_preceding_id
            self.vehicles[str(vehicle_id)].right_alongside_id = right_alongside_id
            self.vehicles[str(vehicle_id)].right_following_id = right_following_id
            self.vehicles[str(vehicle_id)].current_lane = lane_id

        self._remove_vehicles_that_are_out_of_frame()
        self.gui.update_time_in_gui(self.t, self.frame_number)
        self.gui.update_all_graphics_positions()

    def get_all_vehicle_ids(self):
        return self.sim_data.track_meta_data.index.to_numpy()
