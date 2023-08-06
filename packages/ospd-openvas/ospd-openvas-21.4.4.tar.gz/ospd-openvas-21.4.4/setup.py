# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ospd', 'ospd.command', 'ospd_openvas', 'tests', 'tests.command']

package_data = \
{'': ['*']}

modules = \
['ospd-openvas', 'CHANGELOG', 'COPYING', 'poetry']
install_requires = \
['defusedxml>=0.6,<0.8',
 'deprecated>=1.2.10,<2.0.0',
 'lxml>=4.5.2,<5.0.0',
 'packaging>=20.4,<21.0',
 'paramiko>=2.7.1,<3.0.0',
 'psutil>=5.5.1,<6.0.0',
 'redis>=3.5.3,<4.0.0']

entry_points = \
{'console_scripts': ['ospd-openvas = ospd_openvas.daemon:main']}

setup_kwargs = {
    'name': 'ospd-openvas',
    'version': '21.4.4',
    'description': 'ospd based scanner for openvas',
    'long_description': '![Greenbone Logo](https://www.greenbone.net/wp-content/uploads/gb_logo_resilience_horizontal.png)\n\n# ospd-openvas\n\n[![GitHub releases](https://img.shields.io/github/release/greenbone/ospd-openvas.svg)](https://github.com/greenbone/ospd-openvas/releases)\n[![PyPI](https://img.shields.io/pypi/v/ospd-openvas.svg)](https://pypi.org/project/ospd-openvas/)\n[![code test coverage](https://codecov.io/gh/greenbone/ospd/branch/stable/graphs/badge.svg)](https://codecov.io/gh/greenbone/ospd-openvas)\n[![Build and test](https://github.com/greenbone/ospd-openvas/actions/workflows/ci-python.yml/badge.svg?branch=stable)](https://github.com/greenbone/ospd-openvas/actions/workflows/ci-python.yml?query=branch%stable++)\n\nThis is an OSP server implementation to allow GVM to remotely control\nOpenVAS, see <https://github.com/greenbone/openvas>.\n\nOnce running, you need to configure OpenVAS for the Greenbone Vulnerability\nManager, for example via the web interface Greenbone Security Assistant. Then\nyou can create scan tasks to use OpenVAS.\n\n## Installation\n\n### Requirements\n\nPython 3.7 and later is supported.\n\nBeyond the [ospd base library](https://github.com/greenbone/ospd),\n`ospd-openvas` has dependencies on the following Python packages:\n\n- `redis`\n- `psutil`\n- `packaging`\n\nThere are no special installation aspects for this module beyond the general\ninstallation guide for ospd-based scanners.\n\nPlease follow the general installation guide for ospd-based scanners:\n\n  <https://github.com/greenbone/ospd/blob/stable/doc/INSTALL-ospd-scanner.md>\n\n### Mandatory configuration\n\nThe `ospd-openvas` startup parameter `--lock-file-dir` or the `lock_file_dir` config\nparameter of the `ospd.conf` config file needs to point to the same location / path of\nthe `gvmd` daemon and the `openvas` command line tool (Default: `<install-prefix>/var/run`).\nExamples for both are shipped within the `config` sub-folder of this project.\n\nPlease see the `Details` section of the [GVM release notes](https://community.greenbone.net/t/gvm-20-08-stable-initial-release-2020-08-12/6312)\nfor more details.\n\n### Optional configuration\n\nPlease note that although you can run `openvas` (launched from an `ospd-openvas`\nprocess) as a user without elevated privileges, it is recommended that you start\n`openvas` as `root` since a number of Network Vulnerability Tests (NVTs) require\nroot privileges to perform certain operations like packet forgery. If you run\n`openvas` as a user without permission to perform these operations, your scan\nresults are likely to be incomplete.\n\nAs `openvas` will be launched from an `ospd-openvas` process with sudo,\nthe next configuration is required in the sudoers file:\n\n    sudo visudo\n\nadd this line to allow the user running `ospd-openvas`, to launch `openvas`\nwith root permissions\n\n    <user> ALL = NOPASSWD: <install prefix>/sbin/openvas\n\nIf you set an install prefix, you have to update the path in the sudoers\nfile too:\n\n    Defaults        secure_path=<existing paths...>:<install prefix>/sbin\n\n## Usage\n\nThere are no special usage aspects for this module beyond the generic usage\nguide.\n\nPlease follow the general usage guide for ospd-based scanners:\n\n  <https://github.com/greenbone/ospd/blob/stable/doc/USAGE-ospd-scanner.md>\n\n## Support\n\nFor any question on the usage of ospd-openvas please use the [Greenbone\nCommunity Portal](https://community.greenbone.net/c/gse). If you found a problem\nwith the software, please [create an\nissue](https://github.com/greenbone/ospd-openvas/issues) on GitHub. If you are a\nGreenbone customer you may alternatively or additionally forward your issue to\nthe Greenbone Support Portal.\n\n## Maintainer\n\nThis project is maintained by [Greenbone Networks\nGmbH](https://www.greenbone.net/).\n\n## Contributing\n\nYour contributions are highly appreciated. Please [create a pull\nrequest](https://github.com/greenbone/ospd-openvas/pulls) on GitHub. Bigger\nchanges need to be discussed with the development team via the [issues section\nat GitHub](https://github.com/greenbone/ospd-openvas/issues) first.\n\nFor development you should use [poetry](https://python-poetry.org)\nto keep you python packages separated in different environments. First install\npoetry via pip\n\n    python3 -m pip install --user poetry\n\nAfterwards run\n\n    poetry install\n\nin the checkout directory of ospd-openvas (the directory containing the\n`pyproject.toml` file) to install all dependencies including the packages only\nrequired for development.\n\nThe ospd-openvas repository uses [autohooks](https://github.com/greenbone/autohooks)\nto apply linting and auto formatting via git hooks. Please ensure the git hooks\nare active.\n\n    poetry install\n    poetry run autohooks activate --force\n\n## License\n\nCopyright (C) 2018-2021 [Greenbone Networks GmbH](https://www.greenbone.net/)\n\nLicensed under the [GNU Affero General Public License v3.0 or later](COPYING).\n',
    'author': 'Greenbone Networks GmbH',
    'author_email': 'info@greenbone.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/greenbone/ospd-openvas',
    'packages': packages,
    'package_data': package_data,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
