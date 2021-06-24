Put data from the PNeuma project in this folder.
More information on the PNEuma dataset and how to obtain a copy can be found here: https://open-traffic.epfl.ch/.

Please note that due to the size of PNeuma data, this visualizer can only handle the data of 1 drone at one timeslot per file.

Please use the following folder structure:

- data
    |
    - HighD
    |
    - Pneuma
        |
    - data
        |
        (create folder per date, with format yyyymmdd, and put all *.csv files there. see example below)
        |
        - 20181030
            |
            - 20181030_d9_0930_1000.csv
        |
        - README.txt
    |
    - NGSim
