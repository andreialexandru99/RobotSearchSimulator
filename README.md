# RobotSearchSimulator
## Description
This project simulates the deployment of multiple robots in a field with the aim of finding a location where certain pre-established conditions are met.

The field is simulated using a Perlin noise model generated using the project found at https://github.com/pvigier/perlin-numpy. This provides gradual changes in the readings instead of complete randomness.

The robots move randomly and communicate with each other within a certain range to speed up the search. Once one robot has found a satisfactory location, it lets all the others know. The search ends once all robots know of a satisfactory location.

## Installation
1. The project depends on the Perlin noise generator package found at https://github.com/pvigier/perlin-numpy. Follow the installation instructions listed in the project.
2. Install numpy
3. Install matplotlib

## Usage
Run the /src/main.py module to start the search simulation.

To change the search parameters, modify the /src/config.py file as follows:
### App config
- STEP_INTERVAL changes the time interval (in seconds) between each search step. A search step consist of the robots scanning the position they're at, communicating their findings so far to the others and moving to the next location.
- SATISFACTORY_THRESHOLD defines the value above which the search condition is satisfied
- COMMS_RANGE defines the number of tiles between robots within which they can communicate.

### Map config
- MAP_SIZE configures the size of the map, in the same units as COMMS_RANGE
- MAP_RES is a Perlin noise generation parameter. Refer to https://github.com/pvigier/perlin-numpy for further details.
- PERLIN_OCTAVES is a Perlin noise generation parameter. Refer to https://github.com/pvigier/perlin-numpy for further details.

### Robots config
- ROBOTS_COUNT controls the total number of robots included in the search
- ROBOTS_DEPLOY_POINT_X is the point on the X axis where the search begins
- ROBOTS_DEPLOY_POINT_Y is the point on the Y axis where the search begins
- ROBOTS_COLOR_SEARCHING is the color of the dots used to display the location of robots that are still searching
- ROBOTS_COLOR_DONE is the color of the dots used to display the location of robots that are done searching
- ROBOTS_SIZE is the size of the dots used to represent the robots
