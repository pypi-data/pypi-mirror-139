# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pytire']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pytire',
    'version': '0.4.1',
    'description': 'Python library to handle tire attributes.',
    'long_description': '# pytire\n[![Documentation Status](https://readthedocs.org/projects/pytire/badge/?version=latest)](https://pytire.readthedocs.io/en/latest/?badge=latest)\n![Build Status](https://img.shields.io/github/workflow/status/girotobial/pytire/test)\n[![codecov](https://codecov.io/gh/girotobial/pytire/branch/main/graph/badge.svg?token=FRVK7M9PLQ)](https://codecov.io/gh/girotobial/pytire)\n[![PyPI Version](https://img.shields.io/pypi/v/pytire)](https://pypi.org/project/pytire/)\n[![Licence](https://img.shields.io/github/license/girotobial/pytire)](https://github.com/girotobial/pytire/blob/main/LICENSE)\n[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\nA library to make interpreting tire attributes and calculations easier.\n\n### Table of Contents\n  * [Table of Contents](#table-of-contents)\n  * [Getting Started](#getting-started)\n  * [Dev Setup](#dev-setup)\n## Getting Started\nTo use this library install it via pip\n\n```sh\n$ pip install pytire\n```\n\nUsage\n```python\n>>> from pytire import Tire\n>>> tire = Tire("34x10.75-16")\n>>> tire.diameter\n0.8636...\n\n>>> tire.width\n0.27305...\n\n>>> tire.inner_diameter\n0.4064...\n\n>>> tire.volume()\n0.203642044328\n```\n[The Docs are here.](https://pytire.readthedocs.io/en/latest/)\n## Dev Setup\n\nClone from github\n```\n$ git clone \n```\n\nInstall using poetry\n```sh\n$ poetry install\n```\nset up pre-commit\n```sh\n$ pre-commit install\n```\n\nAlternatively use the dev container.\n',
    'author': 'girotobial',
    'author_email': 'abrobinson1907@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/girotobial/pytire',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<3.11',
}


setup(**setup_kwargs)
