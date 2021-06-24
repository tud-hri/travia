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
from dataobjects.enums.annotationtype import AnnotationType


class Annotation:
    def __init__(self, data_set_id):
        self.data_set_id = data_set_id
        self.annotation_type = AnnotationType.MANUAL
        self.first_frame = 0
        self.last_frame = 0
        self.ego_vehicle_id = 0
        self.notes = ""
