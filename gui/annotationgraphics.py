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
from PyQt5 import QtWidgets, QtCore, QtGui


class AnnotationGraphicsObject(QtWidgets.QGraphicsItemGroup):
    def __init__(self, annotation, total_number_of_frames_in_sim, main_gui, parent=None):
        super().__init__(parent)

        self.total_number_of_frames_in_sim = total_number_of_frames_in_sim
        self.annotation = annotation
        self.main_gui = main_gui
        self.start_bar = QtWidgets.QGraphicsLineItem(0.0, 0.0, 0.0, 5.0)
        pen = QtGui.QPen(QtCore.Qt.darkGreen)
        pen.setWidth(1)
        self.start_bar.setPen(pen)

        end_position = round(1000 * (annotation.last_frame - annotation.first_frame) / total_number_of_frames_in_sim)
        self.end_bar = QtWidgets.QGraphicsLineItem(end_position, 0.0, end_position, 5.0)
        pen = QtGui.QPen(QtCore.Qt.red)
        pen.setWidth(1)
        self.end_bar.setPen(pen)

        self.filling = QtWidgets.QGraphicsRectItem(0.0, 0.0, end_position, 5.0)
        self.filling.setPen(QtGui.QPen(QtCore.Qt.NoPen))
        self.filling.setBrush(QtCore.Qt.gray)

        self.addToGroup(self.filling)
        self.addToGroup(self.start_bar)
        self.addToGroup(self.end_bar)

    def mousePressEvent(self, event):
        self.main_gui.select_annotation(self)

    def set_highlight(self, enabled):
        if enabled:
            self.filling.setBrush(QtCore.Qt.blue)
        else:
            self.filling.setBrush(QtCore.Qt.gray)

    def update_borders(self):
        end_position = round(1000 * (self.annotation.last_frame - self.annotation.first_frame) / self.total_number_of_frames_in_sim)
        self.end_bar.setLine(QtCore.QLineF(end_position, 0.0, end_position, 5.0))
        self.filling.setRect(QtCore.QRectF(0.0, 0.0, end_position, 5.0))
