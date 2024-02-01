# Project Computational Science

The formation of clouds is a complex process. This can be simulated with a Cellular
Automata model. This Cellular Automata model tests the influence of relative
humidity and density (Silva, Silva, & Gouvea, 2019). Additionally, wind and
collision effects will be taken into account (Silva et al., 2019), (Dobashi, Kaneda,
Yamashita, Okita, & Nishita, 2000). We will be researching the following question.
What is the influence of humidity and droplet size on the formation of clouds and
the chance of precipitation? The hypothesis is that there is a positive correlation
between rainfall and relative humidity. Evidence from this work suggests a positive
correlation between rainfall and relative humidity.

## Table of Contents
- [Introduction](#introduction)
- [Installation](#installation)
- [Usage](#usage)
- [Credits](#credits)

## Introduction

The formation of clouds is a complex process that can be simulated with a Cellular Automata model. This Cellular Automata model tests the influence of relative humidity and density (Silva, Silva, & Gouvea, 2019). Additionally, wind and collision effects will be taken into account (Silva et al., 2019; Dobashi, Kaneda, Yamashita, Okita, & Nishita, 2000). We will be researching the following question: What is the influence of humidity and droplet size on the formation of clouds and the chance of precipitation? The hypothesis is that there is a positive correlation between rainfall and relative humidity. Evidence from this work suggests a positive correlation between rainfall and relative humidity.

## Installation and Getting Started

1. **Clone the repository**
2. **Install the required dependencies** from `requirements.txt`
3. Go to `wind_and_dropssplitting.py`
4. Read the [Usage](#usage) part
4. **Change the configuration** if necessary
5. **Run** `wind_and_dropssplitting.py`

## Usage
`data_visualization.py` usage:
- Add the csv-filename into the "filename" variable
- Run the script with `$ python data_visualization.py`

`wind_and_dropssplitting.py` usage:
- On the bottom, input parameters can be changed accordingly
- Either `run_simulation()` or `animate_CA()` can be used
- `run_simulation()` simulates without showing the Cellular Automata Animation
- `animate_CA()` simulates while showing the Cellular Automata Animation
- Run the script with `$ python wind_and_dropssplitting.py`

## File Descriptions

- `wind_and_dropssplitting.py`: File to simulate the droplets on a CA grid.
- `validation.py`: File to validate the observed data.
- `data_visualization.py`: File to visualize observed data.

## Folders

- `./exported_data`: This folder contains data obtained from the simulation in a CSV format, with the title formatted using parameters used for the run.
- `./figures`: This folder contains figures obtained from the simulation.
- `./validation_data_final` and `./validation_v1`: These folders contain data for the validation of the observations.

## Credits

- Member 1: Iris Mittelstädt
- Member 2: Sven Haarbrink
- Member 3: Veerle Verbeek

## References

Dobashi, Y., Kaneda, K., Yamashita, H., Okita, T., & Nishita, T. (2000). A simple, efficient method for realistic animation of clouds. In Proceedings of the 27th annual conference on computer graphics and interactive techniques (p. 19–28). USA: ACM Press/Addison-Wesley Publishing Co. Retrieved from https://doi.org/10.1145/344779.344795

Silva, A. R., Silva, A. R., & Gouvêa, M. M. (2019). A novel model to simulate cloud dynamics with cellular automaton. Environmental Modelling & Software, 122, 104537. Retrieved from https://www.sciencedirect.com/science/article/pii/S1364815218305000 doi: https://doi.org/10.1016/j.envsoft.2019.104537
