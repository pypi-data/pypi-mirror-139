# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ts_ids_core', 'ts_ids_core.base']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0', 'pydantic>=1.8,<2', 'typing-extensions>=4.0']

entry_points = \
{'console_scripts': ['export-schema = '
                     'ts_ids_core.generate_jsonschema_ids:write_jsonschema_ids']}

setup_kwargs = {
    'name': 'ts-ids-core',
    'version': '0.1.0a1',
    'description': '',
    'long_description': None,
    'author': 'TetraScience',
    'author_email': 'developers@tetrascience.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
