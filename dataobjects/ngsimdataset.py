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
import os
import pandas as pd
from pyproj import CRS, Transformer

from processing.NGSIMsplitting import split_peachtree_data, split_lankershim_data
from processing.kalmansmoothing import smooth_ngsim_data
from dataobjects.enums import NGSimDatasetID
from processing.encryptiontools import load_encrypted_pickle, save_encrypted_pickle

from .dataset import Dataset


class NGSimDataset(Dataset):
    def __init__(self, track_data, dataset_id: NGSimDatasetID):
        self.dataset_id = dataset_id
        self.track_data = track_data
        self.frame_rate = 10.

        self.annotation_data = []

    def save(self):
        self._save_annotations_to_csv()
        save_encrypted_pickle('data/' + self.dataset_id.data_sub_folder + self.dataset_id.data_file_name + '.pkl', self)

    @staticmethod
    def load(dataset_id: NGSimDatasetID):
        file_location = 'data/' + dataset_id.data_sub_folder + dataset_id.data_file_name
        if os.path.isfile(file_location + '.pkl'):
            return load_encrypted_pickle(file_location + '.pkl')
        elif os.path.isfile(file_location + '.csv'):
            dataset = NGSimDataset.read_ngsim_csv(dataset_id)
            dataset.save()
            return dataset
        elif dataset_id in [NGSimDatasetID.PEACHTREE_0400_0415, NGSimDatasetID.PEACHTREE_1245_0100]:
            if os.path.isfile('data/' + dataset_id.data_sub_folder + 'NGSIM_Peachtree_Vehicle_Trajectories.csv'):
                split_peachtree_data()
                dataset = NGSimDataset.read_ngsim_csv(dataset_id)
                dataset.save()
                return dataset
        elif dataset_id in [NGSimDatasetID.LANKERSHIM_0828_0845, NGSimDatasetID.LANKERSHIM_0845_0900]:
            if os.path.isfile('data/' + dataset_id.data_sub_folder + 'NGSIM__Lankershim_Vehicle_Trajectories.csv'):
                split_lankershim_data()
                dataset = NGSimDataset.read_ngsim_csv(dataset_id)
                dataset.save()
                return dataset

        raise FileNotFoundError('The data file containing the data for ' + str(dataset_id) + ' could not be found at ./data/' + dataset_id.data_sub_folder +
                                ' . Please read the documentation to find out where to find the data and where to put it.')

    @staticmethod
    def read_ngsim_csv(dataset_id: NGSimDatasetID):
        METERS_PER_US_SURVEY_FOOT = 0.3048006096

        data_in_feet = pd.read_csv('data/' + dataset_id.data_sub_folder + dataset_id.data_file_name + '.csv')
        data_in_m = data_in_feet.copy()

        data_in_m.Local_X *= METERS_PER_US_SURVEY_FOOT
        data_in_m.Local_Y *= METERS_PER_US_SURVEY_FOOT
        data_in_m.Global_X *= METERS_PER_US_SURVEY_FOOT
        data_in_m.Global_Y *= METERS_PER_US_SURVEY_FOOT
        data_in_m.v_Width *= METERS_PER_US_SURVEY_FOOT
        data_in_m.v_Vel *= METERS_PER_US_SURVEY_FOOT
        data_in_m.v_Acc *= METERS_PER_US_SURVEY_FOOT

        try:
            data_in_m['v_Length'] *= METERS_PER_US_SURVEY_FOOT
        except (AttributeError, KeyError):
            # a known typo in some of the NGSim datasets is that v_Length is stored as v_length
            data_in_m['v_Length'] = data_in_m['v_length'] * METERS_PER_US_SURVEY_FOOT
            del data_in_m['v_length']

        try:
            data_in_m['Space_Headway'] *= METERS_PER_US_SURVEY_FOOT
        except (AttributeError, KeyError):
            # a known typo some of the NGSim datasets is that Space_Headway is stored as Space_Hdwy
            data_in_m['Space_Headway'] = data_in_m['Space_Hdwy'] * METERS_PER_US_SURVEY_FOOT
            del data_in_m['Space_Hdwy']

        try:
            data_in_m['Time_Headway']
        except (AttributeError, KeyError):
            # a known typo in some of the NGSim datasets is that Time_Headway is stored as Time_Hdwy
            data_in_m['Time_Headway'] = data_in_m['Time_Hdwy']
            del data_in_m['Time_Hdwy']

        try:
            data_in_m['Preceding']
        except (AttributeError, KeyError):
            # a known typo in some of the NGSim datasets is that Preceding is stored as Preceeding
            data_in_m['Preceding'] = data_in_m['Preceeding']
            del data_in_m['Preceeding']

        crs_NAD_38 = CRS.from_epsg(26967)
        crs_gps = CRS.from_epsg(4326)

        coordinate_transformer = Transformer.from_crs(crs_NAD_38, crs_gps)

        data_in_m['Global_lat'], data_in_m['Global_lon'] = coordinate_transformer.transform(data_in_m.Global_X.to_list(), data_in_m.Global_Y.to_list())

        track_data = smooth_ngsim_data(data_in_m)

        dataset = NGSimDataset(track_data, dataset_id)
        dataset.load_annotations_from_csv()
        return dataset
