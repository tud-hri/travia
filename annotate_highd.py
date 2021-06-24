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
from dataobjects import HighDDataset
from dataobjects.enums import HighDDatasetID
from processing import automaticannotationhighd


if __name__ == '__main__':

    for dataset_id in HighDDatasetID:

        data = HighDDataset.load(dataset_id)

        automaticannotationhighd.detect_all_cars_stuck_behind_a_truck(data)
        automaticannotationhighd.detect_all_lane_changes(data)
        automaticannotationhighd.detect_all_significant_decelerations(data)
        automaticannotationhighd.detect_all_complete_overtakes(data)

        data.save()
        print(str(dataset_id) + ' is done.')
