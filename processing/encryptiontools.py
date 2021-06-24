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
import pickle

from cryptography.fernet import Fernet, InvalidToken


def _get_key():
    home_folder = os.path.expanduser("~")

    if not os.path.isfile(home_folder + '\\.travia\\.traffic_data_key'):
        os.mkdir(home_folder + '\\.travia\\')
        new_key = Fernet.generate_key()
        with open(home_folder + '\\.travia\\.traffic_data_key', 'wb') as file:
            file.write(new_key)
        key = new_key
    else:
        with open(home_folder + '\\.travia\\.traffic_data_key', 'rb') as file:
            key = file.readline()
    return key


def save_encrypted_pickle(file_path, data):
    key = _get_key()

    data_as_bytes = pickle.dumps(data)
    encrypted = Fernet(key).encrypt(data_as_bytes)
    with open(file_path, 'bw') as file:
        file.write(encrypted)


def load_encrypted_pickle(file_path):
    if not os.path.isfile(file_path):
        return None

    key = _get_key()
    with open(file_path, 'br') as file:
        encrypted_data = file.read()
        try:
            data_as_bytes = Fernet(key).decrypt(encrypted_data)
        except InvalidToken:
            raise RuntimeError('The loaded file could not be opened. It might have been saved on a different computer and encrypted with a different key. '
                               'Or the file was corrupted. '
                               'Try removing the pickle file from your data folder and loading the data from the csv files.')
        data = pickle.loads(data_as_bytes)
    return data
