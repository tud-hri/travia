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
import enum
from .datasource import DataSource


class HighDDatasetID(enum.Enum):

    DATASET_01 = 1
    DATASET_02 = 2
    DATASET_03 = 3
    DATASET_04 = 4
    DATASET_05 = 5
    DATASET_06 = 6
    DATASET_07 = 7
    DATASET_08 = 8
    DATASET_09 = 9
    DATASET_10 = 10
    DATASET_11 = 11
    DATASET_12 = 12
    DATASET_13 = 13
    DATASET_14 = 14
    DATASET_15 = 15
    DATASET_16 = 16
    DATASET_17 = 17
    DATASET_18 = 18
    DATASET_19 = 19
    DATASET_20 = 20
    DATASET_21 = 21
    DATASET_22 = 22
    DATASET_23 = 23
    DATASET_24 = 24
    DATASET_25 = 25
    DATASET_26 = 26
    DATASET_27 = 27
    DATASET_28 = 28
    DATASET_29 = 29
    DATASET_30 = 30
    DATASET_31 = 31
    DATASET_32 = 32
    DATASET_33 = 33
    DATASET_34 = 34
    DATASET_35 = 35
    DATASET_36 = 36
    DATASET_37 = 37
    DATASET_38 = 38
    DATASET_39 = 39
    DATASET_40 = 40
    DATASET_41 = 41
    DATASET_42 = 42
    DATASET_43 = 43
    DATASET_44 = 44
    DATASET_45 = 45
    DATASET_46 = 46
    DATASET_47 = 47
    DATASET_48 = 48
    DATASET_49 = 49
    DATASET_50 = 50
    DATASET_51 = 51
    DATASET_52 = 52
    DATASET_53 = 53
    DATASET_54 = 54
    DATASET_55 = 55
    DATASET_56 = 56
    DATASET_57 = 57
    DATASET_58 = 58
    DATASET_59 = 59
    DATASET_60 = 60

    @property
    def data_sub_folder(self):
        return 'HighD/data/'

    @property
    def data_file_name(self):
        return '%02d' % self.value

    @property
    def track_data_file_name(self):
        return '%02d_tracks' % self.value

    @property
    def track_meta_data_file_name(self):
        return '%02d_tracksMeta' % self.value

    @property
    def recording_meta_data_file_name(self):
        return '%02d_recordingMeta' % self.value

    @property
    def map_image_name(self):
        return '%02d_highway' % self.value

    @property
    def map_sub_folder(self):
        return 'HighD/images/'

    @property
    def data_source(self):
        return DataSource.HIGHD

    def __str__(self):
        return 'HighD dataset #%02d' % self.value
