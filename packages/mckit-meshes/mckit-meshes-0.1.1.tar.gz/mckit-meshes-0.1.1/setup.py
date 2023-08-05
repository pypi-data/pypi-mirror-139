# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['mckit_meshes',
 'mckit_meshes.mesh',
 'mckit_meshes.plotting',
 'mckit_meshes.utils']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.1,<9.0.0',
 'h5netcdf>=0.13.1,<0.14.0',
 'multipledispatch>=0.6.0,<0.7.0',
 'numpy>=1.21.4,<2.0.0',
 'openpyxl>=3.0.9,<4.0.0',
 'pandas>=1.3.4,<2.0.0',
 'pyevtk>=1.4.1,<2.0.0',
 'toolz>=0.11.2,<0.12.0',
 'xarray>=0.21.1,<0.22.0']

entry_points = \
{'console_scripts': ['mckit-meshes = mckit_meshes.cli.runner:mckit_meshes']}

setup_kwargs = {
    'name': 'mckit-meshes',
    'version': '0.1.1',
    'description': 'Python tools to work with MCNP meshtallies and weight meshes.',
    'long_description': '==============================================================================\n*mckit_meshes*: to work with MCNP mesh tallies and weight meshes\n==============================================================================\n\n\n\n|Maintained| |License| |Versions| |PyPI| |Docs|\n\n.. contents::\n\n\nNote:\n    This document is in progress.\n\nDescription\n-----------\n\nThe module implements methods to read, merge, inverse, normalize and plot\nMCNP mesh tallies and weight meshes.\n\n.. TODO dvp: apply FISPACT v.5 API and describe here.\n\n\nInstallation\n------------\n\n.. TODO dvp: check and report all possible ways to install (pip, poetry)\n\n\nExamples\n--------\n\n.. TODO\n\nContributing\n------------\n\n.. image:: https://github.com/MC-kit/mckit_meshes/workflows/Tests/badge.svg\n   :target: https://github.com/MC-kit/mckit_meshes/actions?query=workflow%3ATests\n   :alt: Tests\n.. image:: https://codecov.io/gh/MC-kit/mckit_meshes/branch/master/graph/badge.svg?token=wlqoa368k8\n  :target: https://codecov.io/gh/MC-kit/mckit_meshes\n.. image:: https://img.shields.io/badge/code%20style-black-000000.svg\n   :target: https://github.com/psf/black\n.. image:: https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336\n   :target: https://pycqa.github.io/isort/\n.. image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white\n   :target: https://github.com/pre-commit/pre-commit\n   :alt: pre-commit\n\nReferences\n----------\n\n.. TODO dvp: add references to iww-gvr, mckit and used libraries:  poetry, xarray etc\n\n\n.. Substitutions\n\n.. |Maintained| image:: https://img.shields.io/badge/Maintained%3F-yes-green.svg\n   :target: https://github.com/MC-kit/mckit_meshes/graphs/commit-activity\n.. |Tests| image:: https://github.com/MC-kit/mckit_meshes/workflows/Tests/badge.svg\n   :target: https://github.com/MC-kit/mckit_meshes/actions?workflow=Tests\n   :alt: Tests\n.. |License| image:: https://img.shields.io/github/license/MC-kit/mckit_meshes\n   :target: https://github.com/MC-kit/mckit_meshes\n.. |Versions| image:: https://img.shields.io/pypi/pyversions/mckit_meshes\n   :alt: PyPI - Python Version\n.. |PyPI| image:: https://img.shields.io/pypi/v/mckit_meshes\n   :target: https://pypi.org/project/mckit_meshes/\n   :alt: PyPI\n.. |Docs| image:: https://readthedocs.org/projects/mckit_meshes/badge/?version=latest\n   :target: https://mckit_meshes.readthedocs.io/en/latest/?badge=latest\n   :alt: Documentation Status\n',
    'author': 'dvp2015',
    'author_email': 'dmitri_portnov@yahoo.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/MC-kit/mckit-meshes',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
