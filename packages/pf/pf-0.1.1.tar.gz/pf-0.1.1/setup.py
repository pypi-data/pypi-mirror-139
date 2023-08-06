# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pf']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pf',
    'version': '0.1.1',
    'description': 'Project Files templating engine.',
    'long_description': '# Project Files\n\nTemplates for quickly initiating my projects.\n',
    'author': 'Deepak',
    'author_email': 'dmallubhotla+github@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitea.deepak.science/deepak/pf',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
