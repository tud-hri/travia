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
import numpy as np
import pykalman

from PyQt5 import QtWidgets
from dataobjects.enums import VehicleType


def _f(state, wheelbase, dt):
    """
    Transition function, returns new state based on the current state. This is a front axle bicycle model
    state: [x, y, heading, velocity, steering_angle, acceleration]
    """
    new_state = state.copy()
    new_state[0] += np.cos(state[2] + state[4]) * state[3] * dt + 0.5 * np.cos(state[2] + state[4]) * state[5] * dt ** 2
    new_state[1] += np.sin(state[2] + state[4]) * state[3] * dt + 0.5 * np.sin(state[2] + state[4]) * state[5] * dt ** 2
    new_state[2] += state[3] * np.sin(state[4]) / wheelbase * dt
    new_state[3] += state[5] * dt
    return new_state


def _estimate_initial_heading(measured_data):
    """
    Function to estimate the initial heading of a vehicle based on the first meter of movement. It does not matter how many frames it takes for the vehicle to
    move a meter.
    """
    x0 = measured_data[0, 0]
    y0 = measured_data[0, 1]

    estimation_length = 0
    dx = 0
    dy = 0

    try:
        while np.sqrt(dx ** 2 + dy ** 2) < 1.:
            estimation_length += 1
            dx = measured_data[estimation_length, 0] - x0
            dy = measured_data[estimation_length, 1] - y0
    except IndexError:  # not enough frames increase the estimation length, use whatever we've got
        pass

    return np.arctan2(dy, dx)


def smooth_ngsim_data(data):

    def g(state):
        """
        Observation function, returns the observation based on the current state
        state: [x, y, heading, velocity, steering_angle, acceleration]
        """
        observation = state[[True, True, False, True, False, True]]
        return observation

    all_vehicle_ids = data['Vehicle_ID'].unique()
    dt = 0.1

    progress_dialog = QtWidgets.QProgressDialog('Smoothing trajectories and calculating headings', None, 0, len(all_vehicle_ids))
    progress_dialog.setWindowTitle('Processing data')
    progress_dialog.setAutoClose(True)
    progress_dialog.show()
    progress_dialog.setValue(0)
    QtWidgets.QApplication.instance().processEvents()

    for index, vehicle_id in enumerate(all_vehicle_ids):
        vehicle_data = data.loc[data['Vehicle_ID'] == vehicle_id, ['Frame_ID', 'Global_X', 'Global_Y', 'v_Vel', 'v_Acc']].sort_values('Frame_ID')
        measured_data = vehicle_data.loc[:, ['Global_X', 'Global_Y', 'v_Vel', 'v_Acc']].to_numpy()
        vehicle_length = float(data.loc[data['Vehicle_ID'] == vehicle_id, 'v_Length'].mean())

        if len(vehicle_data['Frame_ID']) <= 5:
            print(
                'WARNING: vehicle with ID %d appears in only %d frame(s), smoothing is skipped for this vehicle' % (vehicle_id, len(vehicle_data['Frame_ID'])))
            continue

        theta0 = _estimate_initial_heading(measured_data)
        initial_state_mean = np.array([measured_data[0, 0], measured_data[0, 1], theta0, measured_data[0, 2], 0.0, measured_data[0, 3]])

        wb = 0.7 * vehicle_length

        ukf = pykalman.AdditiveUnscentedKalmanFilter(lambda s: _f(s, wb, dt), g, n_dim_state=6, n_dim_obs=4, transition_covariance=np.eye(6) * 0.005,
                                                     initial_state_mean=initial_state_mean)
        try:
            result_from_smoothing = ukf.smooth(measured_data)
            smoothed_states = result_from_smoothing[0]

            data.loc[vehicle_data.index, 'Smoothed_Global_X'] = smoothed_states[:, 0]
            data.loc[vehicle_data.index, 'Smoothed_Global_Y'] = smoothed_states[:, 1]
            data.loc[vehicle_data.index, 'Smoothed_Heading'] = smoothed_states[:, 2]
            data.loc[vehicle_data.index, 'Smoothed_Vel'] = smoothed_states[:, 3]
        except np.linalg.LinAlgError:
            print('WARNING: smoothing for vehicle with ID %d failed' % vehicle_id)

        progress_dialog.setValue(index)
        QtWidgets.QApplication.instance().processEvents()

    progress_dialog.close()
    QtWidgets.QApplication.instance().processEvents()
    return data


def smooth_pneuma_data(vehicles_df, tracks_total_df, dt):

    def g(state):
        """
        Observation function, returns the observation based on the current state
        state: [x, y, heading, velocity, steering_angle, acceleration]
        """
        observation = state[[True, True, False, True, False, False]]
        return observation

    all_vehicle_ids = vehicles_df['track_id']

    progress_dialog = QtWidgets.QProgressDialog('Smoothing trajectories and calculating headings', None, 0, len(all_vehicle_ids))
    progress_dialog.setWindowTitle('Processing data')
    progress_dialog.setAutoClose(True)
    progress_dialog.show()
    progress_dialog.setValue(0)
    QtWidgets.QApplication.instance().processEvents()

    for index, vehicle_id in enumerate(all_vehicle_ids):
        vehicle_data = tracks_total_df.loc[tracks_total_df['vehicle_id'] == vehicle_id, ['time', 'global_x', 'global_y', 'speed']].sort_values('time')
        vehicle_type = VehicleType.from_string(vehicles_df.loc[vehicles_df['track_id'] == vehicle_id, 'type'].iat[0])

        measured_data = vehicle_data.loc[:, ['global_x', 'global_y', 'speed']].to_numpy()

        _, vehicle_length = vehicle_type.default_size_for_pneuma

        if len(vehicle_data['time']) <= 5:
            print(
                'WARNING: vehicle with ID %d appears in only %d frame(s), smoothing is skipped for this vehicle' % (vehicle_id, len(vehicle_data['time'])))
            continue

        theta0 = _estimate_initial_heading(measured_data)
        initial_state_mean = np.array([measured_data[0, 0], measured_data[0, 1], theta0, measured_data[0, 2], 0.0, 0.0])

        wb = 0.7 * vehicle_length

        ukf = pykalman.AdditiveUnscentedKalmanFilter(lambda s: _f(s, wb, dt), g, n_dim_state=6, n_dim_obs=3, transition_covariance=np.eye(6) * 0.001,
                                                     initial_state_mean=initial_state_mean)
        try:
            result_from_smoothing = ukf.smooth(measured_data)
            smoothed_states = result_from_smoothing[0]

            tracks_total_df.loc[vehicle_data.index, 'smoothed_global_x'] = smoothed_states[:, 0]
            tracks_total_df.loc[vehicle_data.index, 'smoothed_global_y'] = smoothed_states[:, 1]
            tracks_total_df.loc[vehicle_data.index, 'smoothed_heading'] = smoothed_states[:, 2]
            tracks_total_df.loc[vehicle_data.index, 'smoothed_speed'] = smoothed_states[:, 3]
        except np.linalg.LinAlgError:
            print('WARNING: smoothing for vehicle with ID %d failed' % vehicle_id)

        progress_dialog.setValue(index)
        QtWidgets.QApplication.instance().processEvents()

    progress_dialog.close()
    QtWidgets.QApplication.instance().processEvents()
