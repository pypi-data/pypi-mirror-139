# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['materia', 'materia.utils']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.19.4,<2.0.0', 'scipy>=1.5.4,<2.0.0']

setup_kwargs = {
    'name': 'materia-utils',
    'version': '1.0.0',
    'description': 'Utilities for atomistic simulations of materials through Materia.',
    'long_description': '====================\nMateria Utils Module\n====================\n\n.. begin-description\n\n.. image:: https://codecov.io/gh/kijanac/materia-utils/branch/master/graph/badge.svg\n  :target: https://codecov.io/gh/kijanac/materia-utils\n\n.. image:: https://img.shields.io/badge/code%20style-black-000000.svg\n    :target: https://github\n\n**Lightweight utilities for atomistic simulations of materials.**\n\nUtilities for atomistic simulations of materials through Materia.\n\n.. end-description\n\n---------------\nGetting Started\n---------------\n\nInstalling\n----------\n.. begin-installing\n\nFrom `pip <https://pypi.org/project/materia-utils/>`_:\n\n``pip install materia-utils``\n\nFrom `conda <https://anaconda.org/kijana/materia-utils>`_:\n\n``conda install -c conda-forge -c kijana materia-utils``\n\n.. end-installing\n\nDocumentation\n-------------\nSee documentation `here <https://kijanac.github.io/materia-utils/>`_.\n\nExamples\n--------\nSee example scripts in `Examples <https://github.com/kijanac/materia-utils/tree/main/examples>`_.\n\n.. begin-about\n\n-------\nAuthors\n-------\nKi-Jana Carter\n\n-------\nLicense\n-------\nThis project is licensed under the MIT License - see the `LICENSE <https://github.com/kijanac/materia-utils/blob/main/LICENSE>`_ file for details.\n\n.. end-about\n\n.. begin-contributing\n\n------------\nContributing\n------------\nSee `CONTRIBUTING <https://github.com/kijanac/materia-utils/blob/main/CONTRIBUTING.rst>`_.\n\n.. end-contributing',
    'author': 'Ki-Jana Carter',
    'author_email': 'kijana@mit.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/kijanac/luz',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<3.11',
}


setup(**setup_kwargs)
