# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tests', 'unifi_protect_backup']

package_data = \
{'': ['*']}

install_requires = \
['aiocron>=1.8,<2.0', 'click==8.0.1', 'pyunifiprotect>=3.2.1,<4.0.0']

extras_require = \
{'dev': ['tox>=3.20.1,<4.0.0',
         'virtualenv>=20.2.2,<21.0.0',
         'pip>=20.3.1,<21.0.0',
         'twine>=3.3.0,<4.0.0',
         'pre-commit>=2.12.0,<3.0.0',
         'toml>=0.10.2,<0.11.0',
         'bump2version>=1.0.1,<2.0.0',
         'tox-asdf>=0.1.0,<0.2.0'],
 'test': ['black>=21.5b2,<22.0',
          'isort>=5.8.0,<6.0.0',
          'flake8>=3.9.2,<4.0.0',
          'flake8-docstrings>=1.6.0,<2.0.0',
          'mypy>=0.900,<0.901',
          'pytest>=6.2.4,<7.0.0',
          'pytest-cov>=2.12.0,<3.0.0']}

entry_points = \
{'console_scripts': ['unifi-protect-backup = unifi_protect_backup.cli:main']}

setup_kwargs = {
    'name': 'unifi-protect-backup',
    'version': '0.1.0',
    'description': 'Python tool to backup unifi event clips in realtime.',
    'long_description': '# Unifi Protect Backup\n\n\n[![pypi](https://img.shields.io/pypi/v/unifi-protect-backup.svg)](https://pypi.org/project/unifi-protect-backup/)\n[![python](https://img.shields.io/pypi/pyversions/unifi-protect-backup.svg)](https://pypi.org/project/unifi-protect-backup/)\n[![Build Status](https://github.com/ep1cman/unifi-protect-backup/actions/workflows/dev.yml/badge.svg)](https://github.com/ep1cman/unifi-protect-backup/actions/workflows/dev.yml)\n[![codecov](https://codecov.io/gh/ep1cman/unifi-protect-backup/branch/main/graphs/badge.svg)](https://codecov.io/github/ep1cman/unifi-protect-backup)\n\nA Python based tool for backing up Unifi Protect event clips as they occur.\n\n* GitHub: <https://github.com/ep1cman/unifi-protect-backup>\n* PyPI: <https://pypi.org/project/unifi-protect-backup/>\n* Free software: MIT\n\n[![Buy me a coffee](https://www.buymeacoffee.com/assets/img/custom_images/black_img.png)](https://www.buymeacoffee.com/ep1cman)\n\n## Features\n\n- Listens to events in real-time via the Unifi Protect websocket API\n- Supports uploading to a [wide range of storage systems using `rclone`](https://rclone.org/overview/)\n- Performs nightly pruning of old clips\n\n## Requirements\n- Python 3.9+\n- Unifi Protect version 1.20 or higher (as per [`pyunifiproect`](https://github.com/briis/pyunifiprotect))\n- `rclone` installed with at least one remote configured.\n\n## Installation\n\n1. Install `rclone.` Instructions for your platform can be found here: https://rclone.org/install/#quickstart\n2. Configure the `rclone` remote you want to back to. Instructions can be found here: https://rclone.org/docs/#configure\n3. `pip install unifi-protect-backup`\n\n## Usage\n```\nUsage: unifi-protect-backup [OPTIONS]\n\n  A Python based tool for backing up Unifi Protect event clips as they occur.\n\nOptions:\n  --address TEXT                  Address of Unifi Protect instance\n                                  [required]\n  --port INTEGER                  Port of Unifi Protect instance\n  --username TEXT                 Username to login to Unifi Protect instance\n                                  [required]\n  --password TEXT                 Password for Unifi Protect user  [required]\n  --verify-ssl / --no-verify-ssl  Set if you do not have a valid HTTPS\n                                  Certificate for your instance\n  --rclone-destination TEXT       `rclone` destination path in the format\n                                  {rclone remote}:{path on remote}. E.g.\n                                  `gdrive:/backups/unifi_protect`  [required]\n  --retention TEXT                How long should event clips be backed up\n                                  for. Format as per the `--max-age` argument\n                                  of rclone`\n                                  (https://rclone.org/filtering/#max-age-don-\n                                  t-transfer-any-file-older-than-this)\n  -v, --verbose                   How verbose the logging output should be.\n\n                                  None: Only log info messages created by\n                                  `unifi-protect-backup`, and all warnings\n\n                                  -v: Only log info & debug messages created\n                                  by `unifi-protect-backup`, and all warnings\n\n                                  -vv: Log info & debug messages created by\n                                  `unifi-protect-backup`, command output, and\n                                  all warnings\n\n                                  -vvv Log debug messages created by `unifi-\n                                  protect-backup`, command output, all info\n                                  messages, and all warnings\n\n                                  -vvvv: Log debug messages created by `unifi-\n                                  protect-backup` command output, all info\n                                  messages, all warnings, and websocket data\n\n                                  -vvvvv: Log websocket data, command output,\n                                  all debug messages, all info messages and\n                                  all warnings  [x>=0]\n  --help                          Show this message and exit.\n```\n\nThe following environment variables can also be used instead of command line arguments (note, CLI arguments\nalways take priority over environment variables):\n- `UFP_USERNAME`\n- `UFP_PASSWORD`\n- `UFP_ADDRESS`\n- `UFP_PORT`\n- `UFP_SSL_VERIFY`\n- `RCLONE_RETENTION`\n- `RCLONE_DESTINATION`\n\n## Credits\n\nHeavily utilises [`pyunifiproect`](https://github.com/briis/pyunifiprotect) by [@briis](https://github.com/briis/)\n\n\nThis package was created with [Cookiecutter](https://github.com/audreyr/cookiecutter) and the [waynerv/cookiecutter-pypackage](https://github.com/waynerv/cookiecutter-pypackage) project template.\n',
    'author': 'sebastian.goscik',
    'author_email': 'sebastian@goscik.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ep1cman/unifi-protect-backup',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.9.0,<4.0',
}


setup(**setup_kwargs)
