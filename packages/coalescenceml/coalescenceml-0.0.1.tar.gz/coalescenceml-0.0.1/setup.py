# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['coalescenceml', 'coalescenceml.cli']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['coml = coalescenceml.cli.cli:cli']}

setup_kwargs = {
    'name': 'coalescenceml',
    'version': '0.0.1',
    'description': 'An open-source MLOps framework to develop industry-grade production ML pipelines coalescing the MLOps stack under one umbrella.',
    'long_description': '# CoalescenceML\n\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/coalescenceml)](https://pypi.org/project/coalescenceml/)\n[![PyPI Status](https://pepy.tech/badge/coalescenceml)](https://pepy.tech/project/coalescenceml)\n[![codecov](https://codecov.io/gh/bayoumi17m/CoalescenceML/branch/main/graph/badge.svg?token=7QNV6GV4B3)](https://codecov.io/gh/bayoumi17m/CoalescenceML)\n![GitHub](https://img.shields.io/github/license/bayoumi17m/CoalescenceML)\n[![Interrogate](docs/interrogate.svg)](https://interrogate.readthedocs.io/en/latest/)\n![Main Workflow Tests](https://github.com/bayoumi17m/CoalescenceML/actions/workflows/main.yml/badge.svg)\n\n# What is Coalescence ML?\n\n# Why use Coalescence ML?\n\n# Learn more about Coalescence ML\n\n## Learn more about MLOps\n\n# Features\n\n# Getting Started\n\n## Install Coalescence ML\n\n## Quickstart\n\n',
    'author': 'Magd Bayoumi, Rafael Chaves, Elva Gao, Edward Gu, Sanjali Jha, Iris Li, Jerry Sun, Emily Wang, Chelsea Xiong',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
