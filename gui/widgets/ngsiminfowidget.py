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
from .ngsiminfowidget_ui import Ui_VehicleInfo
from .vehicleinfowidget import VehicleInfoWidget
from dataobjects import Vehicle


class NGSimInfoWidget(VehicleInfoWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.ui = Ui_VehicleInfo()
        self.ui.setupUi(self)

    def update_information(self, selected_vehicle: Vehicle):
        self.ui.selectedIDLineEdit.setText('%d' % selected_vehicle.id)
        self.ui.selectedTypeLineEdit.setText(str(selected_vehicle.vehicle_type))
        self.ui.selectedLengthLineEdit.setText('%.2f m' % selected_vehicle.length)
        self.ui.selectedWidthLineEdit.setText('%.2f m' % selected_vehicle.width)
        self.ui.selectedXPosLineEdit.setText('%.2f m' % selected_vehicle.current_position[0])
        self.ui.selectedYPosLineEdit.setText('%.2f m' % selected_vehicle.current_position[1])
        self.ui.selectedVeLineEdit.setText('%.2f m/s' % selected_vehicle.current_forward_velocity)
        self.ui.selectedAccLineEdit.setText('%.2f m/s^2' % selected_vehicle.current_forwards_acceleration)
        self.ui.spaceHeadwayLineEdit.setText('%.2f m' % selected_vehicle.dhw)
        self.ui.timeHeadwayLineEdit.setText('%.2f s' % selected_vehicle.thw)
        self.ui.movementLineEdit.setText('%d' % selected_vehicle.movement)
        self.ui.headingLineEdit.setText('%.3f rad' % selected_vehicle.current_heading)
        self.ui.precedingIDLineEdit.setText('%d' % selected_vehicle.preceding_id)
        self.ui.followingIDLineEdit.setText('%d' % selected_vehicle.following_id)
        self.ui.intersectionLineEdit.setText('%d' % selected_vehicle.intersection)
        self.ui.sectionLineEdit.setText('%d' % selected_vehicle.section)
        self.ui.originZoneLineEdit.setText('%d' % selected_vehicle.origin_zone)
        self.ui.destinationZoneLineEdit.setText('%d' % selected_vehicle.destination_zone)
        self.ui.selectedLaneNumLineEdit.setText('%d' % selected_vehicle.current_lane)
        self.ui.directionLineEdit.setText('%d' % selected_vehicle.driving_direction)
