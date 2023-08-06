# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['send2any']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.22.0,<0.23.0']

setup_kwargs = {
    'name': 'send2any',
    'version': '0.1.0',
    'description': 'An unified notification sender sdk',
    'long_description': '# Send2Any\n\n![readthedocs](https://readthedocs.org/projects/send2any/badge/?version=latest)\n![PyPI - Format](https://img.shields.io/pypi/format/nb_workflows)\n![PyPI - Status](https://img.shields.io/pypi/status/nb_workflows)\n\n[![Latest PyPI version](https://img.shields.io/pypi/v/send2any.svg)](https://pypi.python.org/pypi/send2any)\n[![Python versions](https://img.shields.io/pypi/pyversions/send2any.svg)](https://pypi.python.org/pypi/send2any)\n[![Version status](https://img.shields.io/pypi/status/send2any.svg)](https://pypi.python.org/pypi/send2any)\n[![Apache-2.0](https://img.shields.io/pypi/l/send2any.svg)](https://raw.githubusercontent.com/nuxion/main/LICENSE)\n\n[![Documentation](https://readthedocs.org/projects/send2any/badge/?version=latest)](http://send2any.readthedocs.io/en/latest/?badge=latest)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)\n\n\n## Description \n\nA notification library around  services like slack, discord, traditional email, and so forth.\n\nThe goal is to provide an unified api between different services when possible. \n\nFuthermore, whenever possible, the project will try to use only bare bones http requests before any third party library. \n\n## Resources\n\n- [Slack API docs](https://api.slack.com/authentication/basics)\n',
    'author': 'nuxion',
    'author_email': 'nuxion@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/nuxion/sent2any',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.10',
}


setup(**setup_kwargs)
