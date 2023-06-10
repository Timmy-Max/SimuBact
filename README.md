# SimuBact
# Python course project, Dec 2022.
A simple implementation of natural selection. Each bacterium is controlled by a neural network that provides input distances to the centers of mass of food and other bacteria. Then the network outputs weights for each of the directions and they are multiplied by the vectors of the centers of mass and the vector of motion is selected. Learning occurs due to natural selection (adapted survive and transmit genes), as well as due to mutations in genes (neural network weights).
Red bacteria can only eat green bacteria. Green bacteria only eat food scattered across the screen. Each bacterium has its own speed, attack and defense, as well as size. These parameters can mutate during reproduction.
## Dependencies
python version 3.9, pygame version 2.1.2 and numpy version 1.23.5 can be installed manually. There are decent chances that everything will work with older versions but it was never tested.
