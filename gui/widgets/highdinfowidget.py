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
from .highdinfowidget_ui import Ui_VehicleInfo
from .vehicleinfowidget import VehicleInfoWidget


class HighDInfoWidget(VehicleInfoWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.ui = Ui_VehicleInfo()
        self.ui.setupUi(self)

    def update_information(self, selected_vehicle):
        self.ui.selectedIDLineEdit.setText('%d' % selected_vehicle.id)
        self.ui.selectedTypeLineEdit.setText(str(selected_vehicle.vehicle_type))
        self.ui.selectedLengthLineEdit.setText('%.2f m' % selected_vehicle.length)
        self.ui.selectedWidthLineEdit.setText('%.2f m' % selected_vehicle.width)
        self.ui.selectedXPosLineEdit.setText('%.2f m' % selected_vehicle.current_position[0])
        self.ui.selectedYPosLineEdit.setText('%.2f m' % selected_vehicle.current_position[1])
        self.ui.selectedXVeLineEdit.setText('%.2f m/s' % selected_vehicle.current_linear_velocities[0])
        self.ui.selectedYVelLineEdit.setText('%.2f m/s' % selected_vehicle.current_linear_velocities[1])
        self.ui.selectedXAccLineEdit.setText('%.2f m/s^2' % selected_vehicle.current_linear_accelerations[0])
        self.ui.selectedYAccLineEdit.setText('%.2f m/s^2' % selected_vehicle.current_linear_accelerations[1])
        self.ui.selectedFrontSDLineEdit.setText('%.2f m' % selected_vehicle.front_sight_distance)
        self.ui.selectedBackSDLineEdit.setText('%.2f m' % selected_vehicle.back_sight_distance)
        self.ui.selectedDHWLineEdit.setText('%.2f m' % selected_vehicle.dhw)
        self.ui.selectedTHWLineEdit.setText('%.2f s' % selected_vehicle.thw)
        self.ui.selectedTTCLineEdit.setText('%.2f s' % selected_vehicle.ttc)
        self.ui.precedingXVelLineEdit.setText('%.2f m/s' % selected_vehicle.preceding_x_velocity)
        self.ui.precedingIDLineEdit.setText('%d' % selected_vehicle.preceding_id)
        self.ui.followingIDLineEdit.setText('%d' % selected_vehicle.following_id)
        self.ui.leftPrecedingIDLineEdit.setText('%d' % selected_vehicle.left_preceding_id)
        self.ui.leftAlongSideIDLineEdit.setText('%d' % selected_vehicle.left_alongside_id)
        self.ui.leftFollowingIDLineEdit.setText('%d' % selected_vehicle.left_following_id)
        self.ui.rightPrecedingIDLineEdit.setText('%d' % selected_vehicle.right_preceding_id)
        self.ui.rightAlongsideIDLineEdit.setText('%d' % selected_vehicle.right_alongside_id)
        self.ui.rightFollowingIDLineEdit.setText('%d' % selected_vehicle.right_following_id)
        self.ui.selectedLaneNumLineEdit.setText('%d' % selected_vehicle.current_lane)
        self.ui.selectedNumLCLineEdit.setText('%d' % selected_vehicle.number_of_lane_changes)
