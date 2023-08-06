# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['ipl_stats']

package_data = \
{'': ['*']}

install_requires = \
['altair>=4.2.0,<5.0.0',
 'chart-studio>=1.1.0,<2.0.0',
 'cufflinks>=0.17.3,<0.18.0',
 'importlib-resources>=5.4.0,<6.0.0',
 'matplotlib>=3.5.1,<4.0.0',
 'pandas>=1.4.1,<2.0.0',
 'plotly>=5.6.0,<6.0.0',
 'seaborn>=0.11.2,<0.12.0',
 'streamlit>=1.5.1,<2.0.0']

entry_points = \
{'console_scripts': ['start = src.ipl_stats.runserver:main']}

setup_kwargs = {
    'name': 'ipl-stats',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'naveengct',
    'author_email': 'naveenrajesh2222@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
