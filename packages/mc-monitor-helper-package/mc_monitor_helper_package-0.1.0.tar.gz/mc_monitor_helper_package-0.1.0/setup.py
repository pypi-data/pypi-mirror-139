# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mc_monitor_helper_package']

package_data = \
{'': ['*']}

install_requires = \
['gql>=2.0.0,<3.0.0']

setup_kwargs = {
    'name': 'mc-monitor-helper-package',
    'version': '0.1.0',
    'description': 'Utility package for setting and updating monte carlo monitors',
    'long_description': '\n# Monte Carlo Monitor Helper\n\nThis project aims to make setting [Monte Carlo](https://www.montecarlodata.com) field tracking monitors for large numbers of tables with the same schema easier and automatable.\n\n[![GPLv3 License](https://img.shields.io/badge/License-GPL%20v3-yellow.svg)](https://opensource.org/licenses/)\n\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n## Documentation\n\nThis package was tested with Monte Carlo connected to a Snowflake DWH. It was not tested for other warehouses.\n\nFor using this project you need:\n\n* [Monte Carlo](ttps://www.montecarlodata.com)\n* A list of tables with the same time column name, you want to enable field health tracking for.\n## Features\n\n- Set field health tracking automatically for all tables provided\n- Only set tracking for a pre-defined time field\n- Update monitors if they already exist if the respective flag is set, see `example_usage.py`.\n  \n## Installation\n\nInstall this package from PyPi using Pip.\n\n## Usage\n\nSee `example_usage.py`\n',
    'author': 'Gitznik',
    'author_email': 'r.offner@gmx.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Gitznik/monte_carlo_helper_package',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
