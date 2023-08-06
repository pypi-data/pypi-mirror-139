# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rin',
 'rin.gateway',
 'rin.models',
 'rin.models.assets',
 'rin.models.builders',
 'rin.models.channels',
 'rin.models.guild',
 'rin.models.interactions',
 'rin.models.message',
 'rin.models.message.components',
 'rin.rest',
 'rin.utils']

package_data = \
{'': ['*'], 'rin': ['typings/*', 'typings/gateway/*']}

install_requires = \
['aiohttp>=3.8.1,<4.0.0',
 'python-magic>=0.4.25,<0.5.0',
 'typing-extensions>=4.0.1,<5.0.0']

setup_kwargs = {
    'name': 'rin',
    'version': '0.1.2',
    'description': 'A successor to the Lefi project',
    'long_description': '<div align="center">\n    <h1>Rin</h1>\n    <p>\n        <a href="https://rin.readthedocs.io/en/latest/"><img src="https://img.shields.io/readthedocs/rin"</img></a>\n        <a href="https://pypi.org/project/rin/"><img src="https://img.shields.io/pypi/dm/rin"</img></a>\n        <a href="https://codecov.io/gh/an-dyy/Rin"><img src="https://codecov.io/gh/an-dyy/Rin/branch/master/graph/badge.svg?token=G0UG26MRYO"/></a>\n        <a href="https://discord.com/invite/QPFXzFbqrK"><img src="https://img.shields.io/discord/907106240537169980?label=discord"</img></a>\n        <a href="https://github.com/an-dyy/Rin/releases"><img src="https://img.shields.io/github/v/release/an-dyy/rin?include_prereleases&sort=semver"</img></a>\n    </p>\n    A strongly typed discord API wrapper. This is the successor to the Lefi project.\n</div>\n\n## Installation\n\n### Installing from GitHub\n```\npip install -U git+https://github.com/an-dyy/Rin\n```\n\n### Installing from Pypi\nNote that since the project is still unstable, the lastest pypi version may be behind master by a lot.\n```\npip install -U rin\n```\n\n## Example(s)\n[Here!](examples/)\n\n## Documentation\n[Documentation](https://rin.readthedocs.io/en/latest/index.html)\n\n## Contributing\n1. If you plan on contributing please open an issue beforehand\n2. Fork the repo, and setup the poetry env (with dev dependencies)\n3. Install pre-commit hooks (*makes it a lot easier for me*)\n    ```\n    pre-commit install\n    ```\n\n## Notable contributors\n\n- [blanketsucks](https://github.com/blanketsucks) - collaborator\n- [an-dyy](https://github.com/an-dyy) - creator and maintainer\n',
    'author': 'an-dyy',
    'author_email': 'andy.development@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/an-dyy/Rin',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
