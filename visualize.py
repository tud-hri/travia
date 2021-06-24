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
import sys

from PyQt5 import QtWidgets

from dataobjects import PNeumaDataset, NGSimDataset, HighDDataset
from dataobjects.enums import DataSource, PNeumaDatasetID, NGSimDatasetID, HighDDatasetID
from gui import TrafficVisualizerGui
from visualisation import NGSimVisualisationMaster, HighDVisualisationMaster, PNeumaVisualisationMaster


def visualize_traffic_data(data, dataset_id, app):

    gui = TrafficVisualizerGui(data)

    if dataset_id.data_source == DataSource.NGSIM:
        start_time = datetime.datetime.fromtimestamp(int(data.track_data.loc[:, 'Global_Time'].min()/1000))
        end_time = datetime.datetime.fromtimestamp(int(data.track_data.loc[:, 'Global_Time'].max()/1000))
        first_frame = data.track_data.loc[:, 'Frame_ID'].min()
        number_of_frames = data.track_data.loc[:, 'Frame_ID'].max() - first_frame
        visualisation_master = NGSimVisualisationMaster(data, gui, start_time, end_time, number_of_frames, first_frame)
    elif dataset_id.data_source == DataSource.HIGHD:
        start_time = data.start_time
        end_time = start_time + datetime.timedelta(milliseconds=int(data.duration * 1000))
        first_frame = data.track_data['frame'].min()
        number_of_frames = data.track_data['frame'].max() - first_frame
        dt = datetime.timedelta(seconds=1 / data.frame_rate)
        visualisation_master = HighDVisualisationMaster(data, gui, start_time, end_time, number_of_frames, first_frame, dt)
    elif dataset_id.data_source == DataSource.PNEUMA:
        visualisation_master = PNeumaVisualisationMaster(data, gui, data.start_time, data.end_time, data.number_of_frames, 0, data.dt * 2, default_frame_step=2)

    gui.register_visualisation_master(visualisation_master)

    exit_code = app.exec_()
    data.save()
    sys.exit(exit_code)


if __name__ == '__main__':
    """
    To visualise data, you need to define the dataset ID. These ID's are predefined in enums and contain information like the file path for the data and images.
    With this ID, it is possible to load the dataset. All projects have their own enum for ID's and class for datasets. Please look at the examples below to see
    how to load a dataset. 
    """
    app = QtWidgets.QApplication(sys.argv)

    "For loading a HighD dataset, uncomment the next two lines: "
    # dataset_id = HighDDatasetID.DATASET_01
    # data = HighDDataset.load(dataset_id)

    "For loading a NGSIM dataset, uncomment the next two lines: "
    dataset_id = NGSimDatasetID.US101_0805_0820
    data = NGSimDataset.load(dataset_id)

    "For loading a PNeuma dataset, uncomment the next two lines: "
    # dataset_id = PNeumaDatasetID.D181029_T1000_1030_DR8
    # data = PNeumaDataset.load(dataset_id)

    visualize_traffic_data(data, dataset_id, app)
