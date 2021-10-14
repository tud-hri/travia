import random
import unittest

import numpy as np

from dataobjects import Vehicle


class TestPositionConversion(unittest.TestCase):

    def test_position_conversion(self):
        vehicle_length = random.uniform(3.5, 8.)
        vehicle_width = random.uniform(0.4 * vehicle_length, 0.6 * vehicle_length)

        vehicle = Vehicle()
        vehicle.width = vehicle_width
        vehicle.length = vehicle_length

        center_position = np.array([random.uniform(-100., 100.), random.uniform(-100., 100.)])
        heading = random.uniform(-np.pi, np.pi)

        vehicle.current_heading = heading

        vehicle.set_pos_from_center_position(center_position, heading)

        self.assertAlmostEqual(vehicle.center_position[0], center_position[0])
        self.assertAlmostEqual(vehicle.center_position[1], center_position[1])
