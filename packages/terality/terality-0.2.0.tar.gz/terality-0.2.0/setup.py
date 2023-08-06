# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['terality', 'terality_bin']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['terality = terality_bin:main']}

setup_kwargs = {
    'name': 'terality',
    'version': '0.2.0',
    'description': 'The Data Processing Engine for Data Scientists',
    'long_description': 'Terality is the serverless & lightning fast Python data processing engine.\n\nTerality’s engine enable data scientists and engineers to transform and manipulate data at light speed, with the exact same syntax as Pandas, with zero server management.\n\nYou will need a Terality account to use this package. Check out our documentation to get started: https://docs.terality.com/.\n',
    'author': 'Terality Engineering Team',
    'author_email': 'dev.null@terality.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://terality.com/',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<3.7.1',
}


setup(**setup_kwargs)
