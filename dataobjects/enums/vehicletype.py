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
from PyQt5 import QtGui
import enum


class VehicleType(enum.Enum):
    CAR = 1
    TRUCK = 2
    MOTOR_CYCLE = 3
    TAXI = 4
    BUS = 5
    MEDIUM_VEHICLE = 6
    HEAVY_VEHICLE = 7
    PEDESTRIAN = 8
    BICYCLE = 9
    VAN = 10

    def __str__(self):
        return {VehicleType.CAR: 'car',
                VehicleType.TRUCK: 'truck',
                VehicleType.MOTOR_CYCLE: 'motorcycle',
                VehicleType.TAXI: 'taxi',
                VehicleType.BUS: 'bus',
                VehicleType.MEDIUM_VEHICLE: 'heavy vehicle',
                VehicleType.HEAVY_VEHICLE: 'medium vehicle',
                VehicleType.PEDESTRIAN: 'pedestrian',
                VehicleType.BICYCLE: 'bicycle',
                VehicleType.VAN: 'van'
                }[self]

    @property
    def gui_color(self):
        return {VehicleType.CAR: QtGui.QColor(0x945e00),
                VehicleType.TRUCK: QtGui.QColor(0x009479),
                VehicleType.MOTOR_CYCLE: QtGui.QColor(0x8f007e),
                VehicleType.TAXI: QtGui.QColor(0xdeda00),
                VehicleType.BUS: QtGui.QColor(0x0061b0),
                VehicleType.MEDIUM_VEHICLE: QtGui.QColor(0x00705c),
                VehicleType.HEAVY_VEHICLE: QtGui.QColor(0x00d1ac),
                VehicleType.PEDESTRIAN: QtGui.QColor(0xa60000),
                VehicleType.BICYCLE: QtGui.QColor(0xc900b2),
                VehicleType.VAN: QtGui.QColor(0x633f00),
                }[self]

    @property
    def default_size_for_pneuma(self):
        """
        PNeuma does not contain vehicle size, so default sizes must be used. This property returns (vehicle_width, vehicle_length) in meters.
        """
        return {VehicleType.CAR: (2.0, 4.5),
                VehicleType.TRUCK: (2.5, 8.0),
                VehicleType.MOTOR_CYCLE: (0.5, 1.5),
                VehicleType.TAXI: (2.0, 4.5),
                VehicleType.BUS: (2.5, 12.0),
                VehicleType.MEDIUM_VEHICLE: (2.5, 8.0),
                VehicleType.HEAVY_VEHICLE: (2.5, 12.0),
                VehicleType.PEDESTRIAN: (.5, .5),
                VehicleType.BICYCLE: (0.5, 1.5),
                VehicleType.VAN: (2.5, 8.0),
                }[self]

    @staticmethod
    def from_string(string_representation):
        for vehicle_type in VehicleType:
            if string_representation.lower().strip() == str(vehicle_type):
                return vehicle_type
        return None

    @staticmethod
    def from_ngsim_value(value):
        if value == 1:
            return VehicleType.MOTOR_CYCLE
        elif value == 2:
            return VehicleType.CAR
        elif value == 3:
            return VehicleType.TRUCK
        return None
