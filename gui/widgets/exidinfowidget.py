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
from .exidinfowidget_ui import Ui_VehicleInfo
from .vehicleinfowidget import VehicleInfoWidget


class ExidInfoWidget(VehicleInfoWidget):
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
        self.ui.selectedXVelLineEdit.setText('%.2f m/s' % selected_vehicle.current_linear_velocities[0])
        self.ui.selectedYVelLineEdit.setText('%.2f m/s' % selected_vehicle.current_linear_velocities[1])
        self.ui.selectedXAccLineEdit.setText('%.2f m/s^2' % selected_vehicle.current_linear_accelerations[0])
        self.ui.selectedYAccLineEdit.setText('%.2f m/s^2' % selected_vehicle.current_linear_accelerations[1])
        self.ui.selectedLonVelLineEdit.setText('%.2f m/s' % selected_vehicle.current_lon_velocity)
        self.ui.selectedLatVelLineEdit.setText('%.2f m/s' % selected_vehicle.current_lat_velocity)
        self.ui.selectedLonAccLineEdit.setText('%.2f m/s^2' % selected_vehicle.current_lon_acceleration)
        self.ui.selectedLatAccLineEdit.setText('%.2f m/s^2' % selected_vehicle.current_lat_acceleration)
