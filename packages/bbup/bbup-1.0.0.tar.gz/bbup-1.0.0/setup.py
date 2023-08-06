# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bbup']

package_data = \
{'': ['*']}

install_requires = \
['b2sdk>=1.14.0,<2.0.0',
 'colorama>=0.4.4,<0.5.0',
 'requests>=2.27.1,<3.0.0',
 'typer[all]>=0.4.0,<0.5.0',
 'validators>=0.18.1,<0.19.0']

entry_points = \
{'console_scripts': ['bbup = bbup.main:app']}

setup_kwargs = {
    'name': 'bbup',
    'version': '1.0.0',
    'description': '',
    'long_description': '# BackBlaze Uploader\n\nMore description will be added here.',
    'author': 'Rehmat Alam',
    'author_email': 'contact@rehmat.works',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
