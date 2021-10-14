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
import os

import numpy as np
import pandas as pd

from dataobjects.enums import ExiDDatasetID
from processing.encryptiontools import save_encrypted_pickle, load_encrypted_pickle
from .dataset import Dataset


class ExiDDataset(Dataset):
    def __init__(self, id: ExiDDatasetID):
        self.dataset_id = id
        self.recording_id = 0
        self.frame_rate = 0
        self.location_id = 0
        self.speed_limit = 0
        self.week_day = 0
        self.start_time = datetime.time()
        self.duration = 0
        self.total_driven_distance = 0
        self.total_driven_time = 0
        self.num_vehicles = 0
        self.num_cars = 0
        self.num_trucks = 0
        self.upper_lane_markings = []
        self.lower_lane_markings = []

        self.track_meta_data = pd.DataFrame()
        self.track_data = pd.DataFrame()

        self.annotation_data = []

    def save(self):
        file_path = os.path.join('data', self.dataset_id.data_sub_folder, self.dataset_id.data_file_name + '.pkl')
        save_encrypted_pickle(file_path, self)

    @staticmethod
    def load(dataset_id: ExiDDatasetID):
        file_location = os.path.join('data', dataset_id.data_sub_folder, dataset_id.data_file_name)
        if os.path.isfile(file_location + '.pkl'):
            return load_encrypted_pickle(file_location + '.pkl')
        else:
            dataset = ExiDDataset.read_exid_csv(dataset_id)
            dataset.save()
            return dataset

    @staticmethod
    def read_exid_csv(dataset_id: ExiDDatasetID):
        dataset = ExiDDataset(dataset_id)
        path_to_csv = os.path.join('data', dataset_id.data_sub_folder, dataset_id.recording_meta_data_file_name + '.csv')
        try:
            recording_meta_data = pd.read_csv(path_to_csv)
        except FileNotFoundError:
            raise ValueError('The dataset ' + str(dataset_id) + ' could not be loaded because the data is missing.')

        dataset.recording_id = int(recording_meta_data.at[0, 'recordingId'])
        dataset.frame_rate = int(recording_meta_data.at[0, 'frameRate'])
        dataset.location_id = int(recording_meta_data.at[0, 'locationId'])
        dataset.speed_limit = recording_meta_data.at[0, 'speedLimit']

        dataset.week_day = recording_meta_data.at[0, 'weekday']
        dataset.start_time = datetime.datetime.strptime(str(recording_meta_data.at[0, 'startTime']), '%H')
        dataset.duration = recording_meta_data.at[0, 'duration']

        dataset.num_tracks = int(recording_meta_data.at[0, 'numTracks'])
        dataset.num_vehicles = int(recording_meta_data.at[0, 'numVehicles'])
        dataset.num_vrus = int(recording_meta_data.at[0, 'numVRUs'])

        dataset.lat_location = recording_meta_data.at[0, 'latLocation']
        dataset.lon_location = recording_meta_data.at[0, 'lonLocation']
        dataset.x_utm_origin = recording_meta_data.at[0, 'xUtmOrigin']
        dataset.y_utm_origin = recording_meta_data.at[0, 'yUtmOrigin']
        dataset.ortho_px_to_meter = recording_meta_data.at[0, 'orthoPxToMeter']

        path_to_meta_csv = os.path.join('data', dataset_id.data_sub_folder, dataset_id.track_meta_data_file_name + '.csv')
        track_meta_data = pd.read_csv(path_to_meta_csv)
        dataset.track_meta_data = track_meta_data.astype({"recordingId": int,
                                                          "trackId": int,
                                                          "initialFrame": int,
                                                          "finalFrame": int,
                                                          "numFrames": int,
                                                          "width": float,
                                                          "length": float,
                                                          "class": str})
        dataset.track_meta_data = dataset.track_meta_data.set_index('trackId')

        path_to_track_data = os.path.join('data', dataset_id.data_sub_folder, dataset_id.track_data_file_name + '.csv')
        track_data = pd.read_csv(path_to_track_data)
        dataset.track_data = track_data.astype({"recordingId": int,
                                                "trackId": int,
                                                "frame": int,
                                                "trackLifetime": int,
                                                "xCenter": float,
                                                "yCenter": float,
                                                "heading": float,
                                                "width": float,
                                                "length": float,
                                                "xVelocity": float,
                                                "yVelocity": float,
                                                "xAcceleration": float,
                                                "yAcceleration": float,
                                                "lonVelocity": float,
                                                "latVelocity": float,
                                                "lonAcceleration": float,
                                                "latAcceleration": float})
        dataset.track_data['heading'] = np.radians(dataset.track_data['heading'])
        dataset.track_data['yCenter'] = dataset.track_data['yCenter'] * -1
        dataset.track_data['yVelocity'] = dataset.track_data['yVelocity'] * -1
        dataset.track_data['yAcceleration'] = dataset.track_data['yAcceleration'] * -1
        dataset.load_annotations_from_csv()
        return dataset
