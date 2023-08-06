# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['hoshmap', 'hoshmap.function', 'hoshmap.serialization', 'hoshmap.value']

package_data = \
{'': ['*']}

install_requires = \
['bson>=0.5.10,<0.6.0',
 'decompyle3>=3.8.0,<4.0.0',
 'dill>=0.3.4,<0.4.0',
 'hosh>=1.211228.2,<2.0.0',
 'lz4>=4.0.0,<5.0.0',
 'orjson>=3.6.7,<4.0.0']

extras_require = \
{'sqla': ['sqlalchemy>=1.4.23,<2.0.0']}

setup_kwargs = {
    'name': 'hoshmap',
    'version': '0.220221.1',
    'description': 'Hosh-based cacheable lazy dict with deterministic predictable universally unique identifiers',
    'long_description': '![test](https://github.com/davips/hoshmap/workflows/test/badge.svg)\n[![codecov](https://codecov.io/gh/davips/hoshmap/branch/main/graph/badge.svg)](https://codecov.io/gh/davips/hoshmap)\n<a href="https://pypi.org/project/hoshmap">\n<img src="https://img.shields.io/pypi/v/hoshmap.svg?label=release&color=blue&style=flat-square" alt="pypi">\n</a>\n![Python version](https://img.shields.io/badge/python-3.8%20%7C%203.9-blue.svg)\n[![license: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)\n\n<!--- [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.5501845.svg)](https://doi.org/10.5281/zenodo.5501845) --->\n[![arXiv](https://img.shields.io/badge/arXiv-2109.06028-b31b1b.svg?style=flat-square)](https://arxiv.org/abs/2109.06028)\n[![API documentation](https://img.shields.io/badge/doc-API%20%28auto%29-a0a0a0.svg)](https://davips.github.io/hoshmap)\n\n# hoshmap\nA cacheable lazy dict with universally unique deterministic identifiers and transparent agnostic persistence.\n\n## This library is the successor of the package [idict](https://pypi.org/project/idict)\nMost of the _idict_ documentation still applies to _hoshmap_\'s _idict_.\n',
    'author': 'davips',
    'author_email': 'dpsabc@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
