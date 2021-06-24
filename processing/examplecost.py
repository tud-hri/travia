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


def cost_function(x, surrounding_vehicles_positions, lane_centers):
    lane_center_feature = sum(np.exp(-0.8 * ((x[1] - lane_centers) ** 2)))
    distance_other_vehicle = (x[0] - surrounding_vehicles_positions[:, 0]) ** 2 + (x[1] - surrounding_vehicles_positions[:, 1]) ** 2
    collision_feature = sum(np.exp(-.3 * distance_other_vehicle))
    return -lane_center_feature + 5 * collision_feature
