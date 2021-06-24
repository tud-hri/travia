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
import pandas as pd

from dataobjects.enums import NGSimDatasetID


def split_peachtree_data():
    """
    The peachtree data is collected in two sets, one between 12:45 - 01:00 pm and the second between 04:00 - 04:15 pm, both on november 8 2006.
    However the data is supplied in one data file with corrupted timestamps. The initial timestamp of both sets is a correct timestamp in seconds since epoch.
    But after that initial timestamp, the time is considered to be in milliseconds and 100 are added every frame, effective increasing the time with 100
    seconds. This results in timestamps overlapping between the two datasets, so the datasets have to be manually separated and the timestamps have to be
    corrected for.
    """

    all_peachtree_data = pd.read_csv('data/' + NGSimDatasetID.PEACHTREE_0400_0415.data_sub_folder + 'NGSIM_Peachtree_Vehicle_Trajectories.csv')

    # Find index of split, From a manual lookup the split between the datasets was found on the entry with Vehicle_ID 2 and Global_Time 1163030500
    split_index = all_peachtree_data.loc[(all_peachtree_data['Global_Time'] == 1163030500) & (all_peachtree_data['Vehicle_ID'] == 2), :].index
    if len(split_index) > 1:
        raise RuntimeError('The loaded peachtree data was not in the format as expected, please split the data manually.')

    split_index = split_index[0]

    peachtree_1245_0100 = all_peachtree_data.loc[:split_index - 1, :].copy()
    peachtree_0400_0415 = all_peachtree_data.loc[split_index:, :].copy()

    # reconstruct the correct timestamps
    for data_set in [peachtree_1245_0100, peachtree_0400_0415]:
        initial_timestamp = data_set.iat[0, 3]
        milli_seconds_since_start = data_set['Global_Time'] - initial_timestamp

        data_set['Global_Time'] = initial_timestamp * 1000 + milli_seconds_since_start

    peachtree_0400_0415.to_csv('data/' + NGSimDatasetID.PEACHTREE_0400_0415.data_sub_folder + NGSimDatasetID.PEACHTREE_0400_0415.data_file_name + '.csv',
                               index=False)
    peachtree_1245_0100.to_csv('data/' + NGSimDatasetID.PEACHTREE_1245_0100.data_sub_folder + NGSimDatasetID.PEACHTREE_1245_0100.data_file_name + '.csv',
                               index=False)


def split_lankershim_data():
    """
    The lankershim data is collected in two sets, one between 08:28 - 08:45 am and the second between 08:45 - 09:00 am, both on june 15 2005.
    However the data is supplied in one data file. The timestamps in this file are correct, in contrary to the peachtree case.
    """

    all_lankershim_data = pd.read_csv('data/' + NGSimDatasetID.LANKERSHIM_0845_0900.data_sub_folder + 'NGSIM__Lankershim_Vehicle_Trajectories.csv')

    # Find index of split, From a manual lookup the split between the datasets was found on the entry with Vehicle_ID 2 and Global_Time 1118936700000
    split_index = all_lankershim_data.loc[(all_lankershim_data['Global_Time'] == 1118936700000) & (all_lankershim_data['Vehicle_ID'] == 2), :].index
    if len(split_index) > 1:
        raise RuntimeError('The loaded lankershim data was not in the format as expected, please split the data manually.')

    split_index = split_index[0]

    lankershim_0828_0845 = all_lankershim_data.loc[:split_index - 1, :].copy()
    lankershim_0845_0900 = all_lankershim_data.loc[split_index:, :].copy()

    lankershim_0828_0845.to_csv('data/' + NGSimDatasetID.LANKERSHIM_0828_0845.data_sub_folder + NGSimDatasetID.LANKERSHIM_0828_0845.data_file_name + '.csv',
                               index=False)
    lankershim_0845_0900.to_csv('data/' + NGSimDatasetID.LANKERSHIM_0845_0900.data_sub_folder + NGSimDatasetID.LANKERSHIM_0845_0900.data_file_name + '.csv',
                               index=False)

