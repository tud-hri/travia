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
import datetime
import time
import os
from PyQt5 import QtWidgets

import numpy as np
import pandas as pd
from pyproj import CRS, Transformer

from dataobjects.enums import PNeumaDatasetID
from processing.encryptiontools import save_encrypted_pickle, load_encrypted_pickle
from processing.kalmansmoothing import smooth_pneuma_data
from .dataset import Dataset


class PNeumaDataset(Dataset):
    def __init__(self, vehicles, track_data, dt: datetime.timedelta, dataset_id):

        self.start_time = dataset_id.start_time
        self.end_time = self.start_time + datetime.timedelta(seconds=track_data['time'].max() - track_data['time'].min())
        self.dt = dt
        self.frame_rate = 1 / dt.total_seconds()
        self.number_of_frames = int((track_data['time'].max() - track_data['time'].min()) * self.frame_rate)

        self.dataset_id = dataset_id
        self.vehicles = vehicles
        self.track_data = track_data

        self.annotation_data = []

    def save(self):
        self._save_annotations_to_csv()
        file_path = os.path.join('data', self.dataset_id.data_sub_folder, self.dataset_id.data_file_name + '.pkl')
        save_encrypted_pickle(file_path, self)

    @staticmethod
    def load(dataset_id: PNeumaDatasetID):
        file_location = os.path.join('data', dataset_id.data_sub_folder, dataset_id.data_file_name)
        if os.path.isfile(file_location + '.pkl'):
            return load_encrypted_pickle(file_location + '.pkl')
        else:
            dataset = PNeumaDataset.read_pneuma_csv(dataset_id)
            dataset.save()
            return dataset

    @staticmethod
    def read_pneuma_csv(dataset_id: PNeumaDatasetID):
        vehicles = []
        tracks = []

        crs_web_mercator = CRS.from_epsg(3857)
        crs_gps = CRS.from_epsg(4326)
        coordinate_transformer = Transformer.from_crs(crs_gps, crs_web_mercator)

        # get number of lines in file first
        file_path = os.path.join('data', dataset_id.data_sub_folder, dataset_id.data_file_name + '.csv')
        with open(file_path, 'r') as file:
            lines = len([line for line in file])

        progress_dialog = QtWidgets.QProgressDialog('Converting PNeuma csv to data frame', None, 0, lines)
        progress_dialog.setWindowTitle('Processing data')
        progress_dialog.setAutoClose(True)
        progress_dialog.show()
        progress_dialog.setValue(0)
        QtWidgets.QApplication.instance().processEvents()

        with open(file_path, 'r') as file:
            for index, line in enumerate(file):
                if not index:
                    # store the header
                    as_list = line.replace('\n', '').split(';')
                    header_list = [header.strip() for header in as_list[4::]]
                    vehicle_header = [header.strip() for header in as_list[0:4]]
                else:
                    as_list = line.replace('\n', '').split(';')
                    vehicle = [int(as_list[0]), str(as_list[1]), float(as_list[2]), float(as_list[3])]
                    vehicles.append(vehicle)

                    x_list = []
                    y_list = []
                    time_data_only = np.array([float(value) for value in as_list[4:-1]])
                    time_data_only.resize(int(len(time_data_only) / 6), 6)

                    for row in time_data_only:
                        x, y = coordinate_transformer.transform(row[0], row[1])
                        x_list.append(x)
                        y_list.append(y)

                    tracks_df = pd.DataFrame(time_data_only, columns=header_list)
                    tracks_df['vehicle_id'] = pd.Series([vehicle[0]] * len(time_data_only))
                    tracks_df['global_x'] = pd.Series(x_list)
                    tracks_df['global_y'] = pd.Series(y_list)
                    tracks.append(tracks_df)

                    progress_dialog.setValue(index)
                    QtWidgets.QApplication.instance().processEvents()

        vehicles_df = pd.DataFrame(vehicles, columns=vehicle_header)
        tracks_total_df = pd.concat(tracks, axis=0, join='outer', ignore_index=True)

        first_id = vehicles_df['track_id'].iat[0]
        first_time_series = tracks_total_df.loc[tracks_total_df['vehicle_id'] == first_id, 'time']
        dt = datetime.timedelta(seconds=first_time_series.iat[1] - first_time_series.iat[0])

        # convert speed from km/h to m/s
        tracks_total_df['speed'] = tracks_total_df['speed'] / 3.6

        smooth_pneuma_data(vehicles_df, tracks_total_df, dt.total_seconds())
        new_dataset = PNeumaDataset(vehicles_df, tracks_total_df, dt, dataset_id)
        new_dataset.load_annotations_from_csv()
        new_dataset.save()

        progress_dialog.close()
        QtWidgets.QApplication.instance().processEvents()

        return new_dataset
