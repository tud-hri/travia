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
from enum import Enum


class AnnotationType(Enum):
    MANUAL = 0
    CAR_BEHIND_TRUCK = 1
    LANE_CHANGE = 2
    DECELERATION = 3
    COMPLETE_OVERTAKE = 4

    def __str__(self):
        return {AnnotationType.MANUAL: 'Manually created',
                AnnotationType.CAR_BEHIND_TRUCK: 'Car behind a truck',
                AnnotationType.LANE_CHANGE: 'Lane change',
                AnnotationType.DECELERATION: 'Deceleration',
                AnnotationType.COMPLETE_OVERTAKE: 'Complete Overtake', }[self]
