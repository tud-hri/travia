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

from dataobjects.enums import VehicleType


class Vehicle:

    def __init__(self):
        """
        This represents a generic vehicle object, compatible with all datasets. Some data is only available in specific datasets and not in others, like ttc in
        HighD. But no specific child objects for all datasets were made, this object has attributes for all possible data. This was done on purpose to make it
        easier to store your own calculated data if you want to do so. This does mean, that not all attributes of this object will represent correct data in all
        datasets. So be aware that some attributes will always be 0 or None, depending on the dataset you use.

        The origin of this generic vehicle object is located at the middle of the front side; i.e. the middle of the front bumper
        """

        self.id = None
        self.length = None
        self.width = None
        self.first_frame = None
        self.last_frame = None
        self.total_number_of_frames = None
        self.vehicle_type = None
        self.last_time_stamp = 0
        self.current_position = np.array([0.0, 0.0])

        self.dhw = 0.0
        self.thw = 0.0
        self.driving_direction = 0
        self.current_lane = 0
        self.preceding_id = 0
        self.following_id = 0

        # NGSIM specific
        self.movement = 0
        self.intersection = 0
        self.section = 0
        self.origin_zone = 0
        self.destination_zone = 0

        # Pneuma specific
        self.current_lon_acceleration = 0.0
        self.current_lat_acceleration = 0.0

        # HighD specific
        self.current_linear_velocities = np.array([0.0, 0.0])
        self.current_linear_accelerations = np.array([0.0, 0.0])
        self.front_sight_distance = 0.0
        self.back_sight_distance = 0.0
        self.ttc = 0.0
        self.preceding_x_velocity = 0.0
        self.left_preceding_id = 0
        self.left_alongside_id = 0
        self.left_following_id = 0
        self.right_preceding_id = 0
        self.right_alongside_id = 0
        self.right_following_id = 0
        self.number_of_lane_changes = 0

        # NGSim and PNeuma specific
        self.current_heading = 0.0
        self.smoothing_succeeded = False
        self.current_forward_velocity = 0.0
        self.current_forwards_acceleration = 0.0

    def set_pos_from_top_left_corner(self, pos):
        if self.driving_direction == 2:
            pos += np.array([self.length, self.width / 2])
        elif self.driving_direction == 1:
            pos += np.array([0.0, self.width / 2])
        else:
            raise ValueError('Position can only be converted from top left to front bumper center if the driving direction is known. '
                             'This method is meant for use with HighD data only.')
        self.current_position[:] = pos[:]

    @staticmethod
    def from_ngsim_row(first_row, first_frame, last_frame, smoothing_succeeded):
        new_vehicle = Vehicle()

        new_vehicle.id = int(first_row.Vehicle_ID)
        new_vehicle.length = first_row.v_Length
        new_vehicle.width = first_row.v_Width
        new_vehicle.first_frame = int(first_frame)
        new_vehicle.last_frame = int(last_frame)
        new_vehicle.total_number_of_frames = int(first_row.Total_Frames)
        new_vehicle.vehicle_type = VehicleType.from_ngsim_value(first_row.v_Class)
        new_vehicle.smoothing_succeeded = smoothing_succeeded

        return new_vehicle

    @staticmethod
    def from_highd_row(meta_data_row):
        if len(meta_data_row) != 1:
            raise ValueError('A Vehicle object can only be constructed from a single row.')
        index = meta_data_row.index[0]

        new_vehicle = Vehicle()

        new_vehicle.id = index
        new_vehicle.length = float(meta_data_row.at[index, 'width'])
        new_vehicle.width = float(meta_data_row.at[index, 'height'])
        new_vehicle.first_frame = int(meta_data_row.at[index, 'initialFrame'])
        new_vehicle.last_frame = int(meta_data_row.at[index, 'finalFrame'])
        new_vehicle.total_number_of_frames = int(meta_data_row.at[index, 'numFrames'])
        new_vehicle.vehicle_type = VehicleType.from_string(meta_data_row.at[index, 'class'])
        new_vehicle.driving_direction = int(meta_data_row.at[index, 'drivingDirection'])
        new_vehicle.traveled_distance = float(meta_data_row.at[index, 'traveledDistance'])
        new_vehicle.min_x_velocity = float(meta_data_row.at[index, 'minXVelocity'])
        new_vehicle.max_x_velocity = float(meta_data_row.at[index, 'maxXVelocity'])
        new_vehicle.mean_x_velocity = float(meta_data_row.at[index, 'meanXVelocity'])
        new_vehicle.number_of_lane_changes = int(meta_data_row.at[index, 'numLaneChanges'])

        return new_vehicle

    @staticmethod
    def from_pneuma_row(vehicle_row, first_frame, last_frame, smoothing_succeeded):
        new_vehicle = Vehicle()

        new_vehicle.id = int(vehicle_row['track_id'].iat[0])

        new_vehicle.first_frame = int(first_frame)
        new_vehicle.last_frame = int(last_frame)
        new_vehicle.smoothing_succeeded = smoothing_succeeded
        new_vehicle.total_number_of_frames = last_frame - first_frame
        new_vehicle.vehicle_type = VehicleType.from_string(vehicle_row['type'].iat[0])

        new_vehicle.width, new_vehicle.length = new_vehicle.vehicle_type.default_size_for_pneuma

        return new_vehicle

    @property
    def center_position(self):
        return self.current_position - np.array([np.cos(self.current_heading), np.sin(self.current_heading)]) * (self.length/2.0)
