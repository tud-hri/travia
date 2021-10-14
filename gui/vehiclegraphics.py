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
from PyQt5 import QtWidgets, QtGui, QtCore


class VehicleGraphicsObject(QtWidgets.QGraphicsItemGroup):
    def __init__(self, vehicle, main_gui, vehicle_id, parent=None):
        super().__init__(parent)
        self.main_gui = main_gui
        self.vehicle = vehicle
        self.vehicle_id = vehicle_id

        self.bounding_box = QtWidgets.QGraphicsRectItem(-vehicle.length, -vehicle.width / 2, vehicle.length, vehicle.width)

        self.default_color = vehicle.vehicle_type.gui_color
        self.set_highlight(False)

        radius = 0.25
        self.origin = QtWidgets.QGraphicsEllipseItem(-radius, -radius, 2 * radius, 2 * radius)
        self.origin.setPen(QtGui.QPen(QtCore.Qt.NoPen))
        self.origin.setBrush(QtCore.Qt.red)

        self.text = QtWidgets.QGraphicsTextItem(str(vehicle_id))
        font = QtGui.QFont()
        font.setPointSizeF(1.5)
        self.text.setDefaultTextColor(QtCore.Qt.white)
        self.text.setFont(font)
        self.text.setPos(- (vehicle.length / 2) - (self.text.boundingRect().width() / 2), - (self.text.boundingRect().height() / 2))

        self.upside_down_text = QtWidgets.QGraphicsTextItem(str(vehicle_id))
        self.upside_down_text.setDefaultTextColor(QtCore.Qt.white)
        self.upside_down_text.setFont(font)
        self.upside_down_text.setPos(- (self.vehicle.length / 2) + (self.upside_down_text.boundingRect().width() / 2),
                                     (self.upside_down_text.boundingRect().height() / 2))
        self.upside_down_text.setRotation(180)

        self.addToGroup(self.bounding_box)
        self.addToGroup(self.text)
        self.addToGroup(self.upside_down_text)
        self.addToGroup(self.origin)

    def mousePressEvent(self, event):
        self.main_gui.select_vehicle(self.vehicle)

    def set_highlight(self, enabled):
        if enabled:
            self.bounding_box.setPen(QtCore.Qt.blue)
            self.bounding_box.setBrush(QtCore.Qt.blue)
        else:
            self.bounding_box.setPen(self.default_color)
            self.bounding_box.setBrush(self.default_color)

    def setRotation(self, angle: float):
        super(VehicleGraphicsObject, self).setRotation(angle)

        view_rotation_angle = self.main_gui.view.current_rotation

        total_visual_rotation = view_rotation_angle + angle
        while abs(total_visual_rotation) > 180:
            if total_visual_rotation > 0:
                total_visual_rotation -= 360
            else:
                total_visual_rotation += 360

        self.upside_down_text.setVisible(total_visual_rotation > 90.0 or total_visual_rotation < -90.)
        self.text.setVisible(-90. < total_visual_rotation < 90.0)
