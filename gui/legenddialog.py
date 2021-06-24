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
from PyQt5 import QtWidgets, QtCore

from dataobjects.enums import VehicleType
from .legenddialog_ui import Ui_Dialog


class LegendDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self._initialize()
        self.show()

    def _initialize(self):
        for vehicle_type in VehicleType:
            new_label = QtWidgets.QLabel(str(vehicle_type))
            new_label.setAlignment(QtCore.Qt.AlignCenter)

            color_as_rgb_string = "rgb(%d, %d, %d)" % (vehicle_type.gui_color.red(), vehicle_type.gui_color.green(), vehicle_type.gui_color.blue())
            new_label.setStyleSheet("color: white; background-color: " + color_as_rgb_string)

            self.ui.groupBox.layout().addWidget(new_label)
