# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['awsec']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.21.1,<2.0.0', 'rich>=11.2.0,<12.0.0', 'typer>=0.4.0,<0.5.0']

extras_require = \
{'docs': ['sphinx<4',
          'sphinx-click>=2.7,<3.0',
          'sphinx-rtd-theme>=0.5,<0.6',
          'sphinx-autodoc-typehints>=1.12,<2.0']}

setup_kwargs = {
    'name': 'awsec',
    'version': '0.0.1',
    'description': 'A handy little helper for security related tasks in aws',
    'long_description': '# AwSec\n\nWelcome to AwSec. You can find more extensive documentation over at [readthedocs](https://awsec.readthedocs.io/en/latest/).\n\nThis is a small cli tool to make life a little easier for the overworked responder.\n\nContributions are welcome. Just get in touch.\n\n## Quickstart\n\nSimply `pip install awsec` and get going. The cli is available as `awsec` and\nyou can run `awsec --help` to get up to speed on what you can do.\n\n## Development\n\nThis project uses `poetry` for dependency management and `pre-commit` for local checks.\n',
    'author': 'Eduard Thamm',
    'author_email': 'eduard.thamm@thammit.at',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/edthamm/awssec',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
