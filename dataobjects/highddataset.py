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

import pandas as pd

from dataobjects.enums import HighDDatasetID
from processing.encryptiontools import save_encrypted_pickle, load_encrypted_pickle
from .dataset import Dataset


class HighDDataset(Dataset):
    def __init__(self, id: HighDDatasetID):
        self.dataset_id = id
        self.dataset_version = (0, 0)
        self.recording_id = 0
        self.frame_rate = 0
        self.location_id = 0
        self.speed_limit = 0
        self.month = 0
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
    def load(dataset_id: HighDDatasetID):
        file_location = os.path.join('data', dataset_id.data_sub_folder, dataset_id.data_file_name)
        if os.path.isfile(file_location + '.pkl'):
            return load_encrypted_pickle(file_location + '.pkl')
        else:
            dataset = HighDDataset.read_highd_csv(dataset_id)
            dataset.save()
            return dataset

    @staticmethod
    def read_highd_csv(dataset_id: HighDDatasetID):
        dataset = HighDDataset(dataset_id)

        with open(os.path.join('data', dataset_id.path_to_change_log)) as f:
            version = f.readline().split(' ')[0]
            version = version.replace('v', '').split('.')
            dataset.dataset_version = tuple([int(i) for i in version])

        path_to_csv = os.path.join('data', dataset_id.data_sub_folder, dataset_id.recording_meta_data_file_name + '.csv')
        try:
            recording_meta_data = pd.read_csv(path_to_csv)
        except FileNotFoundError:
            raise ValueError('The dataset ' + str(dataset_id) + ' could not be loaded because the data is missing.')

        dataset.recording_id = int(recording_meta_data.at[0, 'id'])
        dataset.frame_rate = int(recording_meta_data.at[0, 'frameRate'])
        dataset.location_id = int(recording_meta_data.at[0, 'locationId'])
        dataset.speed_limit = recording_meta_data.at[0, 'speedLimit']
        dataset.month = recording_meta_data.at[0, 'month']
        dataset.week_day = recording_meta_data.at[0, 'weekDay']
        dataset.start_time = datetime.datetime.strptime(recording_meta_data.at[0, 'startTime'], '%H:%M')
        dataset.duration = recording_meta_data.at[0, 'duration']
        dataset.total_driven_distance = recording_meta_data.at[0, 'totalDrivenDistance']
        dataset.total_driven_time = recording_meta_data.at[0, 'totalDrivenTime']
        dataset.num_vehicles = int(recording_meta_data.at[0, 'numVehicles'])
        dataset.num_cars = int(recording_meta_data.at[0, 'numCars'])
        dataset.num_trucks = int(recording_meta_data.at[0, 'numTrucks'])
        dataset.upper_lane_markings = [float(value) for value in recording_meta_data.at[0, 'upperLaneMarkings'].split(';')]
        dataset.lower_lane_markings = [float(value) for value in recording_meta_data.at[0, 'lowerLaneMarkings'].split(';')]

        path_to_meta_csv = os.path.join('data', dataset_id.data_sub_folder, dataset_id.track_meta_data_file_name + '.csv')
        track_meta_data = pd.read_csv(path_to_meta_csv)
        dataset.track_meta_data = track_meta_data.astype({"id": int,
                                                          "width": float,
                                                          "height": float,
                                                          "initialFrame": int,
                                                          "finalFrame": int,
                                                          "numFrames": int,
                                                          "class": str,
                                                          "drivingDirection": int,
                                                          "traveledDistance": float,
                                                          "minXVelocity": float,
                                                          "maxXVelocity": float,
                                                          "meanXVelocity": float,
                                                          "minDHW": float,
                                                          "minTHW": float,
                                                          "minTTC": float,
                                                          "numLaneChanges": int})
        dataset.track_meta_data = dataset.track_meta_data.set_index('id')

        path_to_track_data = os.path.join('data', dataset_id.data_sub_folder, dataset_id.track_data_file_name + '.csv')
        track_data = pd.read_csv(path_to_track_data)
        dataset.track_data = track_data.astype({"frame": int,
                                                "id": int,
                                                "x": float,
                                                "y": float,
                                                "width": float,
                                                "height": float,
                                                "xVelocity": float,
                                                "yVelocity": float,
                                                "xAcceleration": float,
                                                "yAcceleration": float,
                                                "frontSightDistance": float,
                                                "backSightDistance": float,
                                                "dhw": float,
                                                "thw": float,
                                                "ttc": float,
                                                "precedingXVelocity": float,
                                                "precedingId": int,
                                                "followingId": int,
                                                "leftPrecedingId": int,
                                                "leftAlongsideId": int,
                                                "leftFollowingId": int,
                                                "rightPrecedingId": int,
                                                "rightAlongsideId": int,
                                                "rightFollowingId": int,
                                                "laneId": int})
        dataset.load_annotations_from_csv()
        return dataset
