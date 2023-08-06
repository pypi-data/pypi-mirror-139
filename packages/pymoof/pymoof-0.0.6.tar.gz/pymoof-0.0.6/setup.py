# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pymoof', 'pymoof.clients', 'pymoof.profiles', 'pymoof.tools', 'pymoof.util']

package_data = \
{'': ['*']}

install_requires = \
['bleak>=0.14.2,<0.15.0',
 'cryptography>=36.0.1,<37.0.0',
 'requests>=2.27.1,<3.0.0']

setup_kwargs = {
    'name': 'pymoof',
    'version': '0.0.6',
    'description': 'Connect to your Vanomof S3/X3 bike',
    'long_description': "# pymoof\n[![ReadTheDocs](https://readthedocs.org/projects/pymoof/badge/?version=latest)](https://pymoof.readthedocs.io/en/latest/) [![PyPI version](https://badge.fury.io/py/pymoof.svg)](https://badge.fury.io/py/pymoof) [![Tests](https://github.com/quantsini/pymoof/actions/workflows/test.yml/badge.svg)](https://github.com/quantsini/pymoof/actions/workflows/test.yml)\n\nConnect to your Vanmoof S3 and X3 through bluetooth.\n\n## Installation\n\nInstall python 3.7+, then use pip to install pymoof.\n`pip install pymoof`\n\n## Usage\n\npymoof was tested to work on MacOS 12.1, Ubuntu 20.04.3 LTS, and a Raspberry Pi 3 b+ running Raspberry Pi OS (32-bit) / 2021-10-30.\n```python\nfrom pymoof.clients.sx3 import SX3Client\nimport bleak\n\n...\n\ndevice = ...\nencryption_key = ...\nuser_key_id = ...\n\nasync with bleak.BleakClient(device) as bleak_client:\n\tclient = SX3Client(bleak_client, encryption_key, user_key_id)\n\tawait client.authenticate()\n```\nYou must have an instantiated [bleak](https://bleak.readthedocs.io/en/latest/) client that is connected to the bike. See `pymoof.tools.discover_bike` to determine which device is your bike and `pymoof.tools.retrieve_encryption_key` to connect to Vanmoof servers to get your encryption key.\n\nSee `example.py` for additional usage.\n\n## Contributing\n\nContributions are welcome and encouraged! Every bit helps and credit will be given.\n\nWays you can help:\n\n### Reporting Bugs\n\nYou can report bugs through the github issue tracker: https://github.com/quantsini/pymoof/issues\n\nUseful information to include when reporting bugs:\n\n* Version of pymoof\n* The operating system where pymoof was used\n* What Vanmoof bike was used\n* Detailed steps on reproducing an issue\n\n### Help with reverse engineering\n\nVanmoof bikes communicate through Bluetooth Low Energy. I've tried my best to get all the BLE GATT UUIDs, however, some reverse engineering is needed to figure out what the payloads represent. I suggest using a packet sniffer like [wireshark](https://www.wireshark.org) to analyze data from the official Vanmoof app and the bike.\n\n### Writing Documentation\n\nGood documentation is always good!\n\n### Getting Started with Development\n\nYou want to contribute? Awesome! Here are some steps to get you up and running.\nThis project uses [Poetry](https://python-poetry.org/docs/master/#installing-with-the-official-installer) for package and dependency management and [tox](https://www.tox.wiki/) for tests.\n\n1. Create a fork of the _pymoof_ github repo.\n2. Clone it locally:\n```\ngit clone git@github.com:<your username>/pymoof.git\n```\n3. Get the [latest version of poetry](https://python-poetry.org), a package and dependency management tool.\n4. Install dependencies\n```\npoetry install\n```\n5. Activate your shell. This should put you in a virtualenv that allows you to run tests.\n```\npoetry shell\n```\n6. You should now be able to run tests and make modifications. You can run tests by running tox under poetry\n```\npoetry run tox\n```\n7. Go forth and make great changes!\n",
    'author': 'Henri Bai',
    'author_email': 'quantsini@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/quantsini/pymoof',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
