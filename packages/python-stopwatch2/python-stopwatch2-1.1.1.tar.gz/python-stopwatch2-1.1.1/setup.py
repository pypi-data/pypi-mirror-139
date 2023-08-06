# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['stopwatch']

package_data = \
{'': ['*']}

install_requires = \
['colorama>=0.4.4,<0.5.0']

setup_kwargs = {
    'name': 'python-stopwatch2',
    'version': '1.1.1',
    'description': 'A simple library to measure code performance.',
    'long_description': '<!-- ================ SOCIAL CARD ================= -->\n\n<p align="center"><img src="https://stopwatch2.vercel.app/social.png" alt="Social Card of Python Stopwatch 2"></p>\n\n<!-- ================= TITLE/DESC ================= -->\n\n# Python Stopwatch 2 ⏱️\n\nThis is a fork from [python-stopwatch](https://pypi.org/project/python-stopwatch/) , which adds static typing and a few other things.\n\n<!-- =================== BADGES =================== -->\n\n[![PyPi Version](https://img.shields.io/pypi/v/python-stopwatch2?&style=for-the-badge)](https://pypi.org/project/python-stopwatch2)\n[![PyPi Downloads](https://img.shields.io/pypi/dm/python-stopwatch2?style=for-the-badge)](https://pypistats.org/packages/python-stopwatch2)\n[![Python Versions](https://img.shields.io/pypi/pyversions/python-stopwatch2?&style=for-the-badge)](https://www.python.org)\n[![Repo Size](https://img.shields.io/github/repo-size/devRMA/python-stopwatch2?&style=for-the-badge)](https://github.com/devRMA/python-stopwatch2)\n[![MIT Licensed](https://img.shields.io/github/license/devRMA/python-stopwatch2?&style=for-the-badge)](https://github.com/devRMA/python-stopwatch2/blob/main/LICENSE)\n[![Stars](https://img.shields.io/github/stars/devRMA/python-stopwatch2?&style=for-the-badge)](https://github.com/devRMA/python-stopwatch2/stargazers)\n[![Contributors](https://img.shields.io/github/contributors/devRMA/python-stopwatch2?&style=for-the-badge)](https://github.com/devRMA/python-stopwatch2/graphs/contributors)\n\n***\n\n[![Tests](https://github.com/devRMA/python-stopwatch2/actions/workflows/tests.yml/badge.svg?branch=main)](https://github.com/devRMA/python-stopwatch2/actions/workflows/tests.yml)\n[![Coverage Status](https://coveralls.io/repos/github/devRMA/python-stopwatch2/badge.svg?&style=for-the-badge)](https://coveralls.io/github/devRMA/python-stopwatch2)\n\n<!-- ========== INSTALLATION AND TESTING ========== -->\n\n## 📥 Installation and usage\n\nThis package requires python 3.7 or higher.\nYou\'ll find installation instructions and full documentation on https://stopwatch2.vercel.app.\n\n## ⚠️ Testing\n\nRun the tests with:\n\n``` bash\npoetry run task test\n```\n\n<!-- =========== CHANGELOG AND LICENSE ============ -->\n\n## ✒️ Changelog\n\nPlease see [CHANGELOG](CHANGELOG.md) for detailed changes for each release.\n\n## 📝 Contributing\n\nPlease see [CONTRIBUTING](.github/CONTRIBUTING.md) for details.\n\n## 📑 License\n\n[MIT](https://opensource.org/licenses/MIT)\n\nCopyright (c) 2021-2022 Jonghwan Hyeon, 2022-present Rafael\n',
    'author': 'Rafael',
    'author_email': 'contact.devrma@gmail.com',
    'maintainer': 'Rafael',
    'maintainer_email': 'contact.devrma@gmail.com',
    'url': 'https://stopwatch2.vercel.app/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
