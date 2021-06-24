Put data from the NGSim project in this folder.
More information on the NGSim dataset and how to obtain a copy can be found here:
https://ops.fhwa.dot.gov/trafficanalysistools/ngsim.htm.


Please use the following folder structure:

- data
    |
    - HighD
    |
    - Pneuma
    |
    - NGSim
        |
        (extract *.zip folders for all locations here, for example see the US-101 data below)
        |
        - US-101-LosAngeles-CA
            |
            - aerial-ortho-photos
                |
                - LA-UniversalStudios.tfw
                |
                - LA-UniversalStudios.tif
            |
            - vehicle-trajectory-data
                |
                - 0750am-0805am
                    |
                    - trajectories-0750am-0805am.csv
                    |
                    - trajectories-0750am-0805am.txt
                |
                - 0805am-0820am
                    |
                    - trajectories-0805am-0820am.csv
                    |
                    - trajectories-0805am-0820am.txt
                |
                - 0820am-0835am
                    |
                    - trajectories-0820am-0835am.csv
                    |
                    - trajectories-0820am-0835am.txt
        |
        - README.txt
