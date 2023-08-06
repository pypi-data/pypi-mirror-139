# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['topsis_calci']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.4,<9.0.0',
 'numpy>=1.22.2,<2.0.0',
 'openpyxl>=3.0.9,<4.0.0',
 'pandas>=1.4.1,<2.0.0']

entry_points = \
{'console_scripts': ['topsis = topsis:cli']}

setup_kwargs = {
    'name': 'topsis-calci',
    'version': '0.2.1',
    'description': '',
    'long_description': '# Topsis Calci\n\nTopsis Calci is a Python package implementing Topsis method for decision analysis.\n\n## Installation\n```\npip install topsis-calci\n```\n\n## Usage\n```\ntopsis input_file weights impacts output_file\n```\n\n**OR**\n\n```\npython topsis.py input_file weights impacts output_file\n```\n\n#### Inputs:-\n* input_file -> "Excel/Csv" file path\n* weights -> Comma seperated integers\n* impacts -> Comma seperated +/- impacts\n* output_file -> output csv file path"\n\n#### Outputs:-\n* Creates a csv file on "output_file" path containing score and Ranks\n\n#### Examples :-\nRefer [Examples](./examples)\n\n## License\nThis Project is Licensed under [**BSD-4-Clause**](./LICENSE.txt)\n',
    'author': 'ritikrajdev',
    'author_email': 'ritikrajdev761@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ritikrajdev/topsic-calci',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
