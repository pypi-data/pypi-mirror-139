# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cyberpunk', 'cyberpunk.storage', 'cyberpunk.transformations']

package_data = \
{'': ['*']}

install_requires = \
['Flask>=2.0.2,<3.0.0',
 'PyYAML>=6.0,<7.0',
 'boto3>=1.20.54,<2.0.0',
 'click>=8.0.3,<9.0.0',
 'gunicorn>=20.1.0,<21.0.0',
 'pydub>=0.25.1,<0.26.0',
 'python-dotenv>=0.19.2,<0.20.0',
 'requests>=2.27.1,<3.0.0']

entry_points = \
{'console_scripts': ['cyberpunk = main:main']}

setup_kwargs = {
    'name': 'cyberpunk',
    'version': '0.2.0',
    'description': 'Audio Processing Server',
    'long_description': '\n# Cyberpunk\n\nAudio Processing Server\n\n![GitHub Workflow Status](https://img.shields.io/github/workflow/status/jonaylor89/cyberpunk/Docker)\n\n[![Run on Google Cloud](https://deploy.cloud.run/button.svg)](https://deploy.cloud.run?git_repo=https://github.com/jonaylor89/cyberpunk)\n\n# Install\n\nWith Poetry\n```sh\ncurl -sSL https://install.python-poetry.org | python3 -\npoetry run main.py\n```\n\nWith Docker\n```\ndocker pull ghcr.io/jonaylor89/cyberpunk:sha256-36a2ec3c572d69b41a096cee07f60f2e07d669846ceb0dd8b9f54d741ecc678c.sig\ndocker run -e PORT=8080 jonaylor/cyberpunk\n```\n\n\n# Features\n\n- [x] Audio Streaming\n\n- [ ] Change encodings (e.g. mp3 -> wav)\n- [x] Audio slicing\n- [ ] Change Volume\n- [ ] Concat Audio\n- [x] Repeat Audio\n- [x] Reverse Audio\n- [ ] Crossfade\n- [ ] Fade in/out\n- [ ] Audio Quality\n- [ ] Audio Tagging\n- [ ] Audio Thumbnails\n- [ ] Mastering Music\n\n- [ ] Sound/Vocal Isolation\n\n- [ ] [Cool ML Stuff](https://github.com/spotify/pedalboard)\n\n- [ ] [File Caching](https://gist.github.com/ruanbekker/75d98a0d5cab5d6a562c70b4be5ba86d)\n\n# Storage Options\n\n- [x] Local\n- [ ] Cloud (e.g. S3)\n- [ ] Blockchain (Audius)\n\n\n# Environment\n\nCYBERPUNK_SECRET: mysecret # secret key for URL signature\n\nAWS_ACCESS_KEY_ID: ...\n\nAWS_SECRET_ACCESS_KEY: ...\n\nAWS_REGION: us-east-1',
    'author': 'Johannes Naylor',
    'author_email': 'jonaylor89@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jonaylor89/cyberpunk',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
