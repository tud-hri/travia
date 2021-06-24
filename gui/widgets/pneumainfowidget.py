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
from .vehicleinfowidget import VehicleInfoWidget
from .pneumainfowidget_ui import Ui_VehicleInfo

from dataobjects import Vehicle

class PNeumaInfoWidget(VehicleInfoWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.ui = Ui_VehicleInfo()
        self.ui.setupUi(self)

    def update_information(self, selected_vehicle: Vehicle):
        self.ui.selectedIDLineEdit.setText('%d' % selected_vehicle.id)
        self.ui.selectedTypeLineEdit.setText(str(selected_vehicle.vehicle_type))
        self.ui.selectedXPosLineEdit.setText('%.2f m' % selected_vehicle.current_position[0])
        self.ui.selectedYPosLineEdit.setText('%.2f m' % selected_vehicle.current_position[1])
        self.ui.selectedVelLineEdit.setText('%.2f m/s' % selected_vehicle.current_forward_velocity)
        self.ui.selectedHeadingLineEdit.setText('%.3f rad' % selected_vehicle.current_heading)
        self.ui.selectedLatAccLineEdit.setText('%.2f m/s^2' % selected_vehicle.current_lat_acceleration)
        self.ui.selectedLonAccLineEdit.setText('%.2f m/s^2' % selected_vehicle.current_lon_acceleration)
