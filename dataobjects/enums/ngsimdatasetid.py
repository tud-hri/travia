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
import enum
from .datasource import DataSource


class NGSimDatasetID(enum.Enum):

    I80_0400_0415 = 0x0001
    I80_0500_0515 = 0x0002
    I80_0515_0530 = 0x0003
    LANKERSHIM_0828_0845 = 0x1001
    LANKERSHIM_0845_0900 = 0x1002
    PEACHTREE_1245_0100 = 0x2001
    PEACHTREE_0400_0415 = 0x2002
    US101_0750_0805 = 0x3001
    US101_0805_0820 = 0x3002
    US101_0820_0835 = 0x3003

    def __str__(self):
        return {NGSimDatasetID.I80_0400_0415: 'I-80 4:00 - 4:15 pm',
                NGSimDatasetID.I80_0500_0515: 'I-80 5:00 - 5:15 pm',
                NGSimDatasetID.I80_0515_0530: 'I-80 5:15 - 5:30 pm',
                NGSimDatasetID.LANKERSHIM_0828_0845: 'Lankershim 08:28 am - 08:45 am',
                NGSimDatasetID.LANKERSHIM_0845_0900: 'Lankershim 08:45 am - 09:00 am',
                NGSimDatasetID.PEACHTREE_1245_0100: 'Peachtree 12:45 - 01:00 pm',
                NGSimDatasetID.PEACHTREE_0400_0415: 'Peachtree 04:00 - 04:15 pm',
                NGSimDatasetID.US101_0750_0805: 'US-101 07:50 - 08:05 am',
                NGSimDatasetID.US101_0805_0820: 'US-101 08:05 - 08:20 am',
                NGSimDatasetID.US101_0820_0835: 'US-101 07:20 - 08:35 am'}[self]

    @property
    def data_source(self):
        return DataSource.NGSIM

    @property
    def data_sub_folder(self):
        if self.value < 0x1000:
            return 'NGSim/I-80-Emeryville-CA/vehicle-trajectory-data/'
        elif self.value < 0x2000:
            return 'NGSim/Lankershim-Boulevard-LosAngeles-CA/'
        elif self.value < 0x3000:
            return 'NGSim/Peachtree-Street-Atlanta-GA/'
        else:
            return 'NGSim/US-101-LosAngeles-CA/vehicle-trajectory-data/'

    @property
    def data_file_name(self):
        return {NGSimDatasetID.I80_0400_0415: '0400pm-0415pm/trajectories-0400-0415',
                NGSimDatasetID.I80_0500_0515: '0500pm-0515pm/trajectories-0500-0515',
                NGSimDatasetID.I80_0515_0530: '0515pm-0530pm/trajectories-0515-0530',
                NGSimDatasetID.LANKERSHIM_0828_0845: 'trajectories-0828am-0845am',
                NGSimDatasetID.LANKERSHIM_0845_0900: 'trajectories-0845am-0900am',
                NGSimDatasetID.PEACHTREE_1245_0100: 'trajectories-1245pm-0100pm',
                NGSimDatasetID.PEACHTREE_0400_0415: 'trajectories-0400pm-0415pm',
                NGSimDatasetID.US101_0750_0805: '0750am-0805am/trajectories-0750am-0805am',
                NGSimDatasetID.US101_0805_0820: '0805am-0820am/trajectories-0805am-0820am',
                NGSimDatasetID.US101_0820_0835: '0820am-0835am/trajectories-0820am-0835am'}[self]

    @property
    def map_sub_folder(self):
        if self.value < 0x1000:
            return 'NGSim/I-80-Emeryville-CA/aerial-ortho-photos/'
        elif self.value < 0x2000:
            return 'NGSim/Lankershim-Boulevard-LosAngeles-CA/aerial-ortho-photos/'
        elif self.value < 0x3000:
            return 'NGSim/Peachtree-Street-Atlanta-GA/aerial-ortho-photos/'
        else:
            return 'NGSim/US-101-LosAngeles-CA/aerial-ortho-photos/'

    @property
    def map_image_name(self):
        if self.value < 0x1000:
            return 'emeryville1'
        elif self.value < 0x2000:
            return 'LA-UniversalCity'
        elif self.value < 0x3000:
            return 'Atlanta-Peachtree'
        else:
            return 'LA-UniversalStudios'
