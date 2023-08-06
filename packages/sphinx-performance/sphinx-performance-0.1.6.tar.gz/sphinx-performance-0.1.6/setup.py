# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sphinx_performance',
 'sphinx_performance.projects.basic',
 'sphinx_performance.projects.needs']

package_data = \
{'': ['*'],
 'sphinx_performance.projects.basic': ['_static/*'],
 'sphinx_performance.projects.needs': ['_static/*']}

install_requires = \
['Jinja2>=3.0.3,<4.0.0', 'click>=8.0.3,<9.0.0', 'rich>=11.2.0,<12.0.0']

entry_points = \
{'console_scripts': ['sphinx-performance = sphinx_performance.main:cli']}

setup_kwargs = {
    'name': 'sphinx-performance',
    'version': '0.1.6',
    'description': '',
    'long_description': '.. image:: https://github.com/useblocks/sphinx-performance/raw/main/docs/_static/sphinx_performance_logo.png\n   :align: center\n   :target: https://sphinx-performance.readthedocs.io/en/latest/\n   :alt: Sphinx-Performance\n\n\nCLI tool to measure the build time of different, freely configurable Sphinx-Projects.\n\nDocs\n----\nSee complete documentation at https://sphinx-performance.readthedocs.io/en/latest/\n\nShowcase\n--------\n.. image:: https://github.com/useblocks/sphinx-performance/raw/main/docs/_static/sphinx_performance_showcase.gif\n   :align: center\n   :target: https://sphinx-performance.readthedocs.io/en/latest/\n   :alt: Sphinx-Preview\n',
    'author': 'team useblocks',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/useblocks/sphinx-performance',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
