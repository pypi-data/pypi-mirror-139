# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['demo']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'unfolded.demo',
    'version': '0.0.1',
    'description': 'Public stub for the private unfolded.demo package',
    'long_description': "# `unfolded.demo`\n\n`unfolded.demo` is a package distributed privately by Unfolded.\n\nThis public stub is intended to protect users from [dependency confusion](https://medium.com/@alex.birsan/dependency-confusion-4a5d60fec610), where it's intended to install the private package, but a user accidentally installs a public package from PyPI instead.\n",
    'author': 'Unfolded',
    'author_email': 'contact@unfolded.ai',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
