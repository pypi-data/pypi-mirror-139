# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['clismo',
 'clismo.automata',
 'clismo.builtin',
 'clismo.compiler',
 'clismo.compiler.parsers',
 'clismo.ia',
 'clismo.lang',
 'clismo.optimization',
 'clismo.sim',
 'clismo.visitors']

package_data = \
{'': ['*']}

install_requires = \
['typer>=0.4.0,<0.5.0']

entry_points = \
{'console_scripts': ['clismo = clismo.main:app']}

setup_kwargs = {
    'name': 'clismo',
    'version': '0.1.0',
    'description': 'Programing language designed por simulating and optimizing client-server like discret events models',
    'long_description': None,
    'author': 'Jorge Morgado Vega',
    'author_email': 'jorge.morgadov@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
