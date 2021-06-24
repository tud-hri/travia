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
import datetime

from .datasource import DataSource


class PNeumaDatasetID(enum.Enum):
    D181024_T0830_0900_DR1 = 0x00021
    D181024_T0900_0930_DR1 = 0x00031
    D181024_T0930_1000_DR1 = 0x00041
    D181024_T1000_1030_DR1 = 0x00051
    D181024_T1030_1100_DR1 = 0x00061

    D181029_T0800_0830_DR1 = 0x00101
    D181029_T0830_0900_DR1 = 0x00201
    D181029_T0900_0930_DR1 = 0x00301
    D181029_T0930_1000_DR1 = 0x00401
    D181029_T1000_1030_DR1 = 0x00501

    D181030_T0800_0830_DR1 = 0x01001
    D181030_T0830_0900_DR1 = 0x02001
    D181030_T0900_0930_DR1 = 0x03001
    D181030_T0930_1000_DR1 = 0x04001
    D181030_T1000_1030_DR1 = 0x05001

    D181101_T0800_0830_DR1 = 0x10001
    D181101_T0830_0900_DR1 = 0x20001
    D181101_T0900_0930_DR1 = 0x30001
    D181101_T0930_1000_DR1 = 0x40001
    D181101_T1000_1030_DR1 = 0x50001

    D181024_T0830_0900_DR2 = 0x00022
    D181024_T0900_0930_DR2 = 0x00032
    D181024_T0930_1000_DR2 = 0x00042
    D181024_T1000_1030_DR2 = 0x00052
    D181024_T1030_1100_DR2 = 0x00062

    D181029_T0800_0830_DR2 = 0x00102
    D181029_T0830_0900_DR2 = 0x00202
    D181029_T0900_0930_DR2 = 0x00302
    D181029_T0930_1000_DR2 = 0x00402
    D181029_T1000_1030_DR2 = 0x00502

    D181030_T0800_0830_DR2 = 0x01002
    D181030_T0830_0900_DR2 = 0x02002
    D181030_T0900_0930_DR2 = 0x03002
    D181030_T0930_1000_DR2 = 0x04002
    D181030_T1000_1030_DR2 = 0x05002

    D181101_T0800_0830_DR2 = 0x10002
    D181101_T0830_0900_DR2 = 0x20002
    D181101_T0900_0930_DR2 = 0x30002
    D181101_T0930_1000_DR2 = 0x40002
    D181101_T1000_1030_DR2 = 0x50002

    D181024_T0830_0900_DR3 = 0x00023
    D181024_T0900_0930_DR3 = 0x00033
    D181024_T0930_1000_DR3 = 0x00043
    D181024_T1000_1030_DR3 = 0x00053
    D181024_T1030_1100_DR3 = 0x00063

    D181029_T0800_0830_DR3 = 0x00103
    D181029_T0830_0900_DR3 = 0x00203
    D181029_T0900_0930_DR3 = 0x00303
    D181029_T0930_1000_DR3 = 0x00403
    D181029_T1000_1030_DR3 = 0x00503

    D181030_T0800_0830_DR3 = 0x01003
    D181030_T0830_0900_DR3 = 0x02003
    D181030_T0900_0930_DR3 = 0x03003
    D181030_T0930_1000_DR3 = 0x04003
    D181030_T1000_1030_DR3 = 0x05003

    D181101_T0800_0830_DR3 = 0x10003
    D181101_T0830_0900_DR3 = 0x20003
    D181101_T0900_0930_DR3 = 0x30003
    D181101_T0930_1000_DR3 = 0x40003
    D181101_T1000_1030_DR3 = 0x50003

    D181024_T0830_0900_DR4 = 0x00024
    D181024_T0900_0930_DR4 = 0x00034
    D181024_T0930_1000_DR4 = 0x00044
    D181024_T1000_1030_DR4 = 0x00054
    D181024_T1030_1100_DR4 = 0x00064

    D181029_T0800_0830_DR4 = 0x00104
    D181029_T0830_0900_DR4 = 0x00204
    D181029_T0900_0930_DR4 = 0x00304
    D181029_T0930_1000_DR4 = 0x00404
    D181029_T1000_1030_DR4 = 0x00504

    D181030_T0800_0830_DR4 = 0x01004
    D181030_T0830_0900_DR4 = 0x02004
    D181030_T0900_0930_DR4 = 0x03004
    D181030_T0930_1000_DR4 = 0x04004
    D181030_T1000_1030_DR4 = 0x05004

    D181101_T0800_0830_DR4 = 0x10004
    D181101_T0830_0900_DR4 = 0x20004
    D181101_T0900_0930_DR4 = 0x30004
    D181101_T0930_1000_DR4 = 0x40004
    D181101_T1000_1030_DR4 = 0x50004

    D181024_T0830_0900_DR5 = 0x00025
    D181024_T0900_0930_DR5 = 0x00035
    D181024_T0930_1000_DR5 = 0x00045
    D181024_T1000_1030_DR5 = 0x00055
    D181024_T1030_1100_DR5 = 0x00065

    D181029_T0800_0830_DR5 = 0x00105
    D181029_T0830_0900_DR5 = 0x00205
    D181029_T0900_0930_DR5 = 0x00305
    D181029_T0930_1000_DR5 = 0x00405
    D181029_T1000_1030_DR5 = 0x00505

    D181030_T0800_0830_DR5 = 0x01005
    D181030_T0830_0900_DR5 = 0x02005
    D181030_T0900_0930_DR5 = 0x03005
    D181030_T0930_1000_DR5 = 0x04005
    D181030_T1000_1030_DR5 = 0x05005

    D181101_T0800_0830_DR5 = 0x10005
    D181101_T0830_0900_DR5 = 0x20005
    D181101_T0900_0930_DR5 = 0x30005
    D181101_T0930_1000_DR5 = 0x40005
    D181101_T1000_1030_DR5 = 0x50005

    D181024_T0830_0900_DR6 = 0x00026
    D181024_T0900_0930_DR6 = 0x00036
    D181024_T0930_1000_DR6 = 0x00046
    D181024_T1000_1030_DR6 = 0x00056
    D181024_T1030_1100_DR6 = 0x00066

    D181029_T0800_0830_DR6 = 0x00106
    D181029_T0830_0900_DR6 = 0x00206
    D181029_T0900_0930_DR6 = 0x00306
    D181029_T0930_1000_DR6 = 0x00406
    D181029_T1000_1030_DR6 = 0x00506

    D181030_T0800_0830_DR6 = 0x01006
    D181030_T0830_0900_DR6 = 0x02006
    D181030_T0900_0930_DR6 = 0x03006
    D181030_T0930_1000_DR6 = 0x04006
    D181030_T1000_1030_DR6 = 0x05006

    D181101_T0800_0830_DR6 = 0x10006
    D181101_T0830_0900_DR6 = 0x20006
    D181101_T0900_0930_DR6 = 0x30006
    D181101_T0930_1000_DR6 = 0x40006
    D181101_T1000_1030_DR6 = 0x50006

    D181024_T0830_0900_DR7 = 0x00027
    D181024_T0900_0930_DR7 = 0x00037
    D181024_T0930_1000_DR7 = 0x00047
    D181024_T1000_1030_DR7 = 0x00057
    D181024_T1030_1100_DR7 = 0x00067

    D181029_T0800_0830_DR7 = 0x00107
    D181029_T0830_0900_DR7 = 0x00207
    D181029_T0900_0930_DR7 = 0x00307
    D181029_T0930_1000_DR7 = 0x00407
    D181029_T1000_1030_DR7 = 0x00507

    D181030_T0800_0830_DR7 = 0x01007
    D181030_T0830_0900_DR7 = 0x02007
    D181030_T0900_0930_DR7 = 0x03007
    D181030_T0930_1000_DR7 = 0x04007
    D181030_T1000_1030_DR7 = 0x05007

    D181101_T0800_0830_DR7 = 0x10007
    D181101_T0830_0900_DR7 = 0x20007
    D181101_T0900_0930_DR7 = 0x30007
    D181101_T0930_1000_DR7 = 0x40007
    D181101_T1000_1030_DR7 = 0x50007

    D181024_T0830_0900_DR8 = 0x00028
    D181024_T0900_0930_DR8 = 0x00038
    D181024_T0930_1000_DR8 = 0x00048
    D181024_T1000_1030_DR8 = 0x00058
    D181024_T1030_1100_DR8 = 0x00068

    D181029_T0800_0830_DR8 = 0x00108
    D181029_T0830_0900_DR8 = 0x00208
    D181029_T0900_0930_DR8 = 0x00308
    D181029_T0930_1000_DR8 = 0x00408
    D181029_T1000_1030_DR8 = 0x00508

    D181030_T0800_0830_DR8 = 0x01008
    D181030_T0830_0900_DR8 = 0x02008
    D181030_T0900_0930_DR8 = 0x03008
    D181030_T0930_1000_DR8 = 0x04008
    D181030_T1000_1030_DR8 = 0x05008

    D181101_T0800_0830_DR8 = 0x10008
    D181101_T0830_0900_DR8 = 0x20008
    D181101_T0900_0930_DR8 = 0x30008
    D181101_T0930_1000_DR8 = 0x40008
    D181101_T1000_1030_DR8 = 0x50008

    D181024_T0830_0900_DR9 = 0x00029
    D181024_T0900_0930_DR9 = 0x00039
    D181024_T0930_1000_DR9 = 0x00049
    D181024_T1000_1030_DR9 = 0x00059
    D181024_T1030_1100_DR9 = 0x00069

    D181029_T0800_0830_DR9 = 0x00109
    D181029_T0830_0900_DR9 = 0x00209
    D181029_T0900_0930_DR9 = 0x00309
    D181029_T0930_1000_DR9 = 0x00409
    D181029_T1000_1030_DR9 = 0x00509

    D181030_T0800_0830_DR9 = 0x01009
    D181030_T0830_0900_DR9 = 0x02009
    D181030_T0900_0930_DR9 = 0x03009
    D181030_T0930_1000_DR9 = 0x04009
    D181030_T1000_1030_DR9 = 0x05009

    D181101_T0800_0830_DR9 = 0x10009
    D181101_T0830_0900_DR9 = 0x20009
    D181101_T0900_0930_DR9 = 0x30009
    D181101_T0930_1000_DR9 = 0x40009
    D181101_T1000_1030_DR9 = 0x50009

    D181024_T0830_0900_DR10 = 0x0002a
    D181024_T0900_0930_DR10 = 0x0003a
    D181024_T0930_1000_DR10 = 0x0004a
    D181024_T1000_1030_DR10 = 0x0005a
    D181024_T1030_1100_DR10 = 0x0006a

    D181029_T0800_0830_DR10 = 0x0010a
    D181029_T0830_0900_DR10 = 0x0020a
    D181029_T0900_0930_DR10 = 0x0030a
    D181029_T0930_1000_DR10 = 0x0040a
    D181029_T1000_1030_DR10 = 0x0050a

    D181030_T0800_0830_DR10 = 0x0100a
    D181030_T0830_0900_DR10 = 0x0200a
    D181030_T0900_0930_DR10 = 0x0300a
    D181030_T0930_1000_DR10 = 0x0400a
    D181030_T1000_1030_DR10 = 0x0500a

    D181101_T0800_0830_DR10 = 0x1000a
    D181101_T0830_0900_DR10 = 0x2000a
    D181101_T0900_0930_DR10 = 0x3000a
    D181101_T0930_1000_DR10 = 0x4000a
    D181101_T1000_1030_DR10 = 0x5000a

    def __str__(self):
        if self.value & 0x000F0:
            date = '18/10/24 '
        elif self.value & 0x00F00:
            date = '18/10/29 '
        elif self.value & 0x0F000:
            date = '18/10/30 '
        else:
            date = '18/11/1 '

        time_identifier = hex(self.value & 0xFFFF0).replace('0', '').replace('x', '')

        if time_identifier == '1':
            time = '08:00-08:30 '
        elif time_identifier == '2':
            time = '08:30-09:00 '
        elif time_identifier == '3':
            time = '09:00-09:30 '
        elif time_identifier == '4':
            time = '09:30-10:00 '
        elif time_identifier == '5':
            time = '10:00-10:30 '
        else:
            time = '10:30-11:00 '

        drone = 'drone %d' % (self.value & 0x0000F)

        return date + time + drone

    @property
    def data_source(self):
        return DataSource.PNEUMA

    @property
    def data_sub_folder(self):
        if self.value & 0x000F0:
            return 'pNeuma/20181024/'
        elif self.value & 0x00F00:
            return 'pNeuma/20181029/'
        elif self.value & 0x0F000:
            return 'pNeuma/20181030/'
        else:
            return 'pNeuma/20181101/'

    @property
    def data_file_name(self):
        if self.value & 0x000F0:
            date = '20181024'
        elif self.value & 0x00F00:
            date = '20181029'
        elif self.value & 0x0F000:
            date = '20181030'
        else:
            date = '20181101'

        time_identifier = hex(self.value & 0xFFFF0).replace('0', '').replace('x', '')

        if time_identifier == '1':
            time = '0800_0830'
        elif time_identifier == '2':
            time = '0830_0900'
        elif time_identifier == '3':
            time = '0900_0930'
        elif time_identifier == '4':
            time = '0930_1000'
        elif time_identifier == '5':
            time = '1000_1030'
        else:
            time = '1030_1100'

        drone = 'd%d' % (self.value & 0x0000F)

        return date + '_' + drone + '_' + time

    @property
    def start_time(self):
        if self.value & 0x000F0:
            date = '2018/10/24 '
        elif self.value & 0x00F00:
            date = '2018/10/29 '
        elif self.value & 0x0F000:
            date = '2018/10/30 '
        else:
            date = '2018/11/01 '

        time_identifier = hex(self.value & 0xFFFF0).replace('0', '').replace('x', '')

        if time_identifier == '1':
            time = '08:00'
        elif time_identifier == '2':
            time = '08:30'
        elif time_identifier == '3':
            time = '09:00'
        elif time_identifier == '4':
            time = '09:30'
        elif time_identifier == '5':
            time = '10:00'
        else:
            time = '10:30'

        return datetime.datetime.strptime(date + time, '%Y/%m/%d %H:%M')

    @property
    def map_sub_folder(self):
        return 'pNeuma/images/'

    @property
    def map_image_name(self):
        return 'pneuma'
