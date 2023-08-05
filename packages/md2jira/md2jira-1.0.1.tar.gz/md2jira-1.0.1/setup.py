# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['md2jira']

package_data = \
{'': ['*']}

install_requires = \
['mistletoe>=0.8.2,<0.9.0']

entry_points = \
{'console_scripts': ['md2jira = md2jira.md2jira:main']}

setup_kwargs = {
    'name': 'md2jira',
    'version': '1.0.1',
    'description': 'Markdown to jira',
    'long_description': '# md2jira\n\n[![PyPI](https://img.shields.io/pypi/v/md2jira)](https://pypi.org/project/md2jira/)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/md2jira)](https://www.python.org/downloads/)\n[![GitHub last commit](https://img.shields.io/github/last-commit/daxartio/md2jira)](https://github.com/daxartio/md2jira)\n[![GitHub stars](https://img.shields.io/github/stars/daxartio/md2jira?style=social)](https://github.com/daxartio/md2jira)\n\n```\npip install md2jira\n```\n\n## Contributing\n\n[Contributing](CONTRIBUTING.md)\n',
    'author': 'Danil Akhtarov',
    'author_email': 'daxartio@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://pypi.org/project/md2jira',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
