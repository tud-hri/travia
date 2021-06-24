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
from dataobjects import HighDDataset, Annotation, AnnotationType
from dataobjects.enums import VehicleType

"""
This file contains functions that automatically find and annotate some specific events in HighD data. It serves both as a tool to detect these events, and as an
example of how this detection could work. From this it should be easy to extend the automatic detects to other dataset or events.
"""


def detect_all_cars_stuck_behind_a_truck(sim_data: HighDDataset):
    number_of_cars = len(sim_data.track_meta_data)
    car_types = [None] * (number_of_cars + 1)

    for car_id in range(1, number_of_cars + 1):
        car_types[car_id] = VehicleType.from_string(sim_data.track_meta_data.at[car_id, 'class'])

    list_of_truck_ids = [i for i, x in enumerate(car_types) if x is VehicleType.TRUCK]

    for car_id in range(1, number_of_cars + 1):
        if car_types[car_id] is VehicleType.CAR:
            car_data = sim_data.track_data.loc[sim_data.track_data.id == car_id, :]

            frames_where_truck_is_followed = car_data.loc[car_data.precedingId.isin(list_of_truck_ids), :]

            if not frames_where_truck_is_followed.empty:
                last_frame = -1

                for index in frames_where_truck_is_followed.index:
                    current_frame = frames_where_truck_is_followed.at[index, 'frame']

                    if last_frame == -1:
                        annotation_fist_frame = current_frame
                    elif current_frame != last_frame + 1:
                        annotation_last_frame = last_frame
                        new_annotation = Annotation(sim_data.recording_id)
                        new_annotation.first_frame = annotation_fist_frame
                        new_annotation.last_frame = annotation_last_frame
                        new_annotation.ego_vehicle_id = car_id
                        new_annotation.annotation_type = AnnotationType.CAR_BEHIND_TRUCK
                        new_annotation.notes = 'AUTOMATIC: Car behind a truck'
                        sim_data.annotation_data.append(new_annotation)
                        annotation_fist_frame = current_frame
                    last_frame = current_frame

                annotation_last_frame = last_frame
                new_annotation = Annotation(sim_data.recording_id)
                new_annotation.first_frame = annotation_fist_frame
                new_annotation.last_frame = annotation_last_frame
                new_annotation.ego_vehicle_id = car_id
                new_annotation.annotation_type = AnnotationType.CAR_BEHIND_TRUCK
                new_annotation.notes = 'AUTOMATIC: Car behind a truck'
                sim_data.annotation_data.append(new_annotation)


def _lane_changes_in(data_frame):
    number_of_lane_changes = 0
    previous_id = data_frame['laneId'].iloc[0]
    for lane_id in data_frame.loc[:, 'laneId'].to_numpy():
        if lane_id != previous_id:
            number_of_lane_changes += 1
        previous_id = lane_id
    return number_of_lane_changes


def detect_all_lane_changes(sim_data: HighDDataset, c=2.0):
    """
    detects all lane changes in a dataset and annotates the part of the trajectory where the y-velocity of a vehicle is higher then its average y-velocity/c.
    Where c is a parameter to tune the length of the annotated bit. By default, c=2.0
    """
    number_of_cars = len(sim_data.track_meta_data)
    for car_id in range(1, number_of_cars + 1):
        car_data = sim_data.track_data.loc[sim_data.track_data.id == car_id, :]

        number_of_lane_changes = _lane_changes_in(car_data)
        if number_of_lane_changes:
            number_of_detected_annotations = 0
            average_y_velocity = car_data.loc[:, 'yVelocity'].abs().mean()

            lane_changing_data = car_data.loc[car_data.yVelocity.abs() >= average_y_velocity / c, :]

            if not lane_changing_data.empty:
                last_frame = -1

                for index in lane_changing_data.index:
                    current_frame = lane_changing_data.at[index, 'frame']

                    if last_frame == -1:
                        annotation_fist_frame = current_frame
                    elif current_frame != last_frame + 1:
                        annotation_last_frame = last_frame
                        data_within_annotation = car_data.loc[(car_data.frame >= annotation_fist_frame) & (car_data.frame <= annotation_last_frame), :]
                        if _lane_changes_in(data_within_annotation):
                            number_of_detected_annotations += _lane_changes_in(data_within_annotation)
                            new_annotation = Annotation(sim_data.recording_id)
                            new_annotation.first_frame = annotation_fist_frame
                            new_annotation.last_frame = annotation_last_frame
                            new_annotation.ego_vehicle_id = car_id
                            new_annotation.annotation_type = AnnotationType.LANE_CHANGE
                            new_annotation.notes = 'AUTOMATIC: Lane Change'
                            sim_data.annotation_data.append(new_annotation)
                        annotation_fist_frame = current_frame
                    last_frame = current_frame
                annotation_last_frame = last_frame
                data_within_annotation = car_data.loc[(car_data.frame >= annotation_fist_frame) & (car_data.frame <= annotation_last_frame), :]
                if _lane_changes_in(data_within_annotation):
                    number_of_detected_annotations += _lane_changes_in(data_within_annotation)
                    new_annotation = Annotation(sim_data.recording_id)
                    new_annotation.first_frame = annotation_fist_frame
                    new_annotation.last_frame = annotation_last_frame
                    new_annotation.ego_vehicle_id = car_id
                    new_annotation.annotation_type = AnnotationType.LANE_CHANGE
                    new_annotation.notes = 'AUTOMATIC: Lane Change'
                    sim_data.annotation_data.append(new_annotation)
            if number_of_lane_changes != number_of_detected_annotations:
                print('Something is wrong with car %d, %d lane changes are made but %d are detected' % (
                car_id, number_of_lane_changes, number_of_detected_annotations))


def detect_all_significant_decelerations(sim_data, c=2.0):
    """
    Automatically detects all negative accelerations (decelerations) in a dataset have a magnitude <= the mean - c * the standard deviation. Where c is a
    parameter to tune the number of selected decelerations. By default, c=2.0 which represents approximately 2.2% of the lowest accelerations.
    """
    std = sim_data.track_data.loc[:, 'xAcceleration'].std()
    mean = sim_data.track_data.loc[:, 'xAcceleration'].mean()

    number_of_cars = len(sim_data.track_meta_data)
    for car_id in range(1, number_of_cars + 1):
        car_data = sim_data.track_data.loc[sim_data.track_data.id == car_id, :]

        frames_where_acc_is_high = car_data.loc[car_data.xAcceleration <= mean - c * std, :]

        if not frames_where_acc_is_high.empty:
            last_frame = -1

            for index in frames_where_acc_is_high.index:
                current_frame = frames_where_acc_is_high.at[index, 'frame']

                if last_frame == -1:
                    annotation_fist_frame = current_frame
                elif current_frame != last_frame + 1:
                    annotation_last_frame = last_frame
                    new_annotation = Annotation(sim_data.recording_id)
                    new_annotation.first_frame = annotation_fist_frame
                    new_annotation.last_frame = annotation_last_frame
                    new_annotation.ego_vehicle_id = car_id
                    new_annotation.annotation_type = AnnotationType.DECELERATION
                    new_annotation.notes = 'AUTOMATIC: High Deceleration'
                    sim_data.annotation_data.append(new_annotation)
                    annotation_fist_frame = current_frame
                last_frame = current_frame

            annotation_last_frame = last_frame
            new_annotation = Annotation(sim_data.recording_id)
            new_annotation.first_frame = annotation_fist_frame
            new_annotation.last_frame = annotation_last_frame
            new_annotation.ego_vehicle_id = car_id
            new_annotation.annotation_type = AnnotationType.DECELERATION
            new_annotation.notes = 'AUTOMATIC: High deceleration'
            sim_data.annotation_data.append(new_annotation)


def detect_all_complete_overtakes(sim_data: HighDDataset):
    number_of_cars = len(sim_data.track_meta_data)
    for car_id in range(1, number_of_cars + 1):
        car_data = sim_data.track_data.loc[sim_data.track_data.id == car_id, :]
        all_frame_numbers = car_data['frame'].to_numpy()

        number_of_lane_changes = _lane_changes_in(car_data)
        if number_of_lane_changes > 1:
            average_y_velocity = car_data.loc[:, 'yVelocity'].abs().mean()
            driving_direction = sim_data.track_meta_data.at[car_id, 'drivingDirection']  # 1 = left, 2 = right

            all_driven_lanes = car_data.loc[:, 'laneId'].unique()
            if driving_direction == 1:  # the highest lane number is the overtake lane
                overtake_lane_data = car_data.loc[car_data.laneId == max(all_driven_lanes), :]
            else:  # the lowest lane number is the overtake lane
                overtake_lane_data = car_data.loc[car_data.laneId == min(all_driven_lanes), :]

            first_frame_in_overtake_lane = overtake_lane_data['frame'].iat[0]
            last_frame_in_overtake_lane = overtake_lane_data['frame'].iat[-1]

            annotation_fist_frame = None
            annotation_last_frame = None

            current_frame = first_frame_in_overtake_lane
            while annotation_fist_frame is None:
                if car_data.loc[car_data.frame == current_frame].yVelocity.abs().iat[0] <= average_y_velocity / 2.0:
                    annotation_fist_frame = current_frame
                else:
                    current_frame -= 1
                    if current_frame not in all_frame_numbers:
                        annotation_fist_frame = current_frame + 1

            current_frame = last_frame_in_overtake_lane
            while annotation_last_frame is None:
                if car_data.loc[car_data.frame == current_frame].yVelocity.abs().iat[0] <= average_y_velocity / 2.0:
                    annotation_last_frame = current_frame
                else:
                    current_frame += 1
                    if current_frame not in all_frame_numbers:
                        annotation_last_frame = current_frame - 1

            if annotation_fist_frame is not None and annotation_last_frame is not None:
                last_frame = -1
                new_annotation = Annotation(sim_data.recording_id)
                new_annotation.first_frame = annotation_fist_frame
                new_annotation.last_frame = annotation_last_frame
                new_annotation.ego_vehicle_id = car_id
                new_annotation.annotation_type = AnnotationType.COMPLETE_OVERTAKE
                new_annotation.notes = 'AUTOMATIC: Complete overtake'
                sim_data.annotation_data.append(new_annotation)

