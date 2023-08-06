# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': '..'}

packages = \
['templateco_cli']

package_data = \
{'': ['*'], 'templateco_cli': ['dist/*']}

install_requires = \
['templateco>=0,<1', 'typer>=0.3,<0.5']

entry_points = \
{'console_scripts': ['templateco = templateco_cli:app']}

setup_kwargs = {
    'name': 'templateco-cli',
    'version': '0.1.1',
    'description': '',
    'long_description': '# Templateco CLI\nA CLI for interacting with Templateco on your local machine.\n',
    'author': 'Mike Gregory',
    'author_email': 'mike.ja.gregory@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
