# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dunamai_formatters']

package_data = \
{'': ['*']}

install_requires = \
['dunamai>=1.9.0,<2.0.0']

setup_kwargs = {
    'name': 'dunamai-formatters',
    'version': '0.0.1',
    'description': 'A complementary tool to Dunamai that offers formatters that can be used as the format argument of the serialize function.',
    'long_description': '# Dunamai formatters\n[![pipeline status](https://gitlab.com/marnik/dunamai-formatters/badges/dev/pipeline.svg)](https://gitlab.com/marnik/dunamai-formatters/-/commits/dev)\n[![coverage report](https://gitlab.com/marnik/dunamai-formatters/badges/dev/coverage.svg)](https://gitlab.com/marnik/dunamai-formatters/-/commits/dev)\n[![codecov](https://codecov.io/gl/marnik/dunamai-formatters/branch/dev/graph/badge.svg?token=O9DSYD0HV1)](https://codecov.io/gl/marnik/dunamai-formatters)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![Security: bandit](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit)\n[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)\n\nA complementary tool to [Dunamai](https://github.com/mtkennerly/dunamai) that offers formatters that can be used as the format argument of the `serialize` function.\n\n## Features\n\n* PEP440 formatters\n\n\n',
    'author': 'Marnik De Bont',
    'author_email': 'marnik@mdebont.be',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://gitlab.com/marnik/dunamai-formatters',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
