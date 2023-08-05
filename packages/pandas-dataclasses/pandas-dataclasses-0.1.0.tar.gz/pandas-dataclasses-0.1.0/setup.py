# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pandas_dataclasses']

package_data = \
{'': ['*']}

install_requires = \
['morecopy>=0.2,<0.3', 'pandas>=1.3,<2.0', 'typing-extensions>=3.10,<4.0']

setup_kwargs = {
    'name': 'pandas-dataclasses',
    'version': '0.1.0',
    'description': 'pandas extension for typed Series and DataFrame creation',
    'long_description': '# pandas-dataclasses\n\n[![PyPI](https://img.shields.io/pypi/v/pandas-dataclasses.svg?label=PyPI&style=flat-square)](https://pypi.org/project/pandas-dataclasses/)\n[![Python](https://img.shields.io/pypi/pyversions/pandas-dataclasses.svg?label=Python&color=yellow&style=flat-square)](https://pypi.org/project/pandas-dataclasses/)\n[![Test](https://img.shields.io/github/workflow/status/astropenguin/pandas-dataclasses/Tests?logo=github&label=Test&style=flat-square)](https://github.com/astropenguin/pandas-dataclasses/actions)\n[![License](https://img.shields.io/badge/license-MIT-blue.svg?label=License&style=flat-square)](LICENSE)\n\npandas extension for typed Series and DataFrame creation\n\n## Installation\n\n```bash\npip install pandas-dataclasses\n```\n',
    'author': 'Akio Taniguchi',
    'author_email': 'taniguchi@a.phys.nagoya-u.ac.jp',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/astropenguin/pandas-dataclasses/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<3.11',
}


setup(**setup_kwargs)
