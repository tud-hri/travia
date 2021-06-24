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
import abc
from PyQt5 import QtWidgets


class VehicleInfoWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

    @abc.abstractmethod
    def update_information(self, selected_vehicle):
        pass

    @property
    def all_line_edits(self):
        return [item for _, item in self.ui.__dict__.items() if isinstance(item, QtWidgets.QLineEdit)]

    def enable_all_fields(self, boolean):
        for line_edit in self.all_line_edits:
            line_edit.setEnabled(boolean)

    def clear_info_fields(self):
        for line_edit in self.all_line_edits:
            line_edit.setText('')
