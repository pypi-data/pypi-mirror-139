
# Monte Carlo Monitor Helper

This project aims to make setting [Monte Carlo](https://www.montecarlodata.com) field tracking monitors for large numbers of tables with the same schema easier and automatable.

[![GPLv3 License](https://img.shields.io/badge/License-GPL%20v3-yellow.svg)](https://opensource.org/licenses/)

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
## Documentation

This package was tested with Monte Carlo connected to a Snowflake DWH. It was not tested for other warehouses.

For using this project you need:

* [Monte Carlo](ttps://www.montecarlodata.com)
* A list of tables with the same time column name, you want to enable field health tracking for.
## Features

- Set field health tracking automatically for all tables provided
- Only set tracking for a pre-defined time field
- Update monitors if they already exist if the respective flag is set, see `example_usage.py`.
  
## Installation

Install this package from PyPi using Pip.

## Usage

See `example_usage.py`
