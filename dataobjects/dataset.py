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
import enum

from .annotation import Annotation
from .enums import AnnotationType


class Dataset(abc.ABC):
    annotation_data: list
    dataset_id: enum.Enum

    def _save_annotations_to_csv(self):
        file_name = 'data/' + self.dataset_id.data_sub_folder + self.dataset_id.data_file_name + '_annotations.csv'
        with open(file_name, 'w') as f:
            f.write('first_frame, last_frame, ego_vehicle_id, annotation_type, notes\n')
            for annotation in self.annotation_data:
                f.write(
                    ', '.join([str(annotation.first_frame), str(annotation.last_frame), str(annotation.ego_vehicle_id), str(annotation.annotation_type.value),
                               annotation.notes.replace(',', ';').replace('\n', '')]) + '\n')

    def load_annotations_from_csv(self):
        try:
            with open('data/' + self.dataset_id.data_sub_folder + self.dataset_id.data_file_name + '_annotations.csv', 'r') as f:
                header = f.readline()
                for line in f:
                    annotations_as_list = line.replace('\n', '').split(', ')
                    if len(annotations_as_list) > 1:
                        new_annotation = Annotation(self.dataset_id)
                        new_annotation.first_frame = int(annotations_as_list[0])
                        new_annotation.last_frame = int(annotations_as_list[1])
                        new_annotation.ego_vehicle_id = int(annotations_as_list[2])

                        new_annotation.annotation_type = AnnotationType(int(annotations_as_list[3]))
                        new_annotation.notes = annotations_as_list[4]

                        self.annotation_data.append(new_annotation)
        except FileNotFoundError:
            print('No annotations file could be found for this dataset')