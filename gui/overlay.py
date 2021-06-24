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
import ctypes

from PyQt5 import QtGui


class Overlay(QtGui.QPixmap):
    def __init__(self, data, width, height):
        """
        A pixmap overlay for the world view, to visualize cost/reward functions or other parameters. The data should be supplied as a table with scalar values.
        All values are converted to pixels in the pixmap. High values will be displayed as red, low values as blue.

        The values are automatically scaled such that the minimum value is full blue and the maximum value is full red. A 24 bit color representation
        (0xRRBBGG) is used, so the values a discretised to a 1024 value color system.

        :param data: scalar data table to be converted to colormap
        :param width: with in pixels
        :param height: height in pixels
        """
        super().__init__(width, height)

        self.data_width = width
        self.data_height = height

        self._set_data(data)

    def _set_data(self, data):
        """
        Convert the data to a colormap, load this as a QImage and convert the QImage to a QPixmap for easy displaying.
        :param data: scalar data table to be converted to colormap
        :return:
        """

        """ map data to integer values from 0 to 4 * 2^8 - 1 (1023), store as unsigned 32 bit integer array """
        min_value = data.min()
        data -= min_value

        max_value = data.max()
        factor = (4 * (2 ** 8) - 1) / max_value
        data *= factor
        data = data.round().astype(ctypes.c_uint32)

        """ Convert discretized data to color map (based on the short rainbow implementation found here: https://www.particleincell.com/2014/colormap/, 
        but not completely the same). Data is split in four groups, and all values are converted to range from 0-255 or 255-0. Then two of the three colors are 
        kept constant for each group, and the third is swapped by the value (in a color representation of 0xFFRRGGBB). This results in the values being mapped  
        to a continues range: 0xFF0000FF - 0xFF00FFFF - 0xFF00FF00 - 0xFFFFFF00 - 0xFFFF0000"""

        rgb_table = data.copy()

        rgb_table[data < 1 * (2 ** 8)] = 0xFF0000FF + data[data < 1 * (2 ** 8)].astype(ctypes.c_uint16) * 2 ** 8
        rgb_table[(data >= 1 * (2 ** 8)) & (data < 2 * (2 ** 8))] = 0xFF00FF00 + (
                -1 * (data[(data >= 1 * (2 ** 8)) & (data < 2 * (2 ** 8))] - 1 * 2 ** 8) + 2 ** 8 - 1).astype(ctypes.c_uint16)
        rgb_table[(data >= 2 * (2 ** 8)) & (data < 3 * (2 ** 8))] = 0xFF00FF00 + (data[(data >= 2 * (2 ** 8)) & (data < 3 * (2 ** 8))] - 2 * (2 ** 8)).astype(
            ctypes.c_uint16) * 2 ** 16
        rgb_table[(data >= 3 * (2 ** 8)) & (data < 4 * (2 ** 8))] = 0xFFFF0000 + (
                -1 * (data[(data >= 3 * (2 ** 8)) & (data < 4 * (2 ** 8))] - 3 * (2 ** 8)) + 2 ** 8 - 1).astype(ctypes.c_uint16) * 2 ** 8

        """ Construct image and set data. """
        im = QtGui.QImage(rgb_table.tobytes(), self.data_width, self.data_height, QtGui.QImage.Format_ARGB32)
        self.convertFromImage(im)
