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
    'version': '1.1.0',
    'description': 'A simple library to measure code performance.',
    'long_description': '<!-- ================ TITLE/DESC ================ -->\n\n<div align=\'center\'>\n    <h2>Python-StopWatch-2</h2>\n    <p>A simple stopwatch for measuring code performance. This is a fork from <a href=\'https://pypi.org/project/python-stopwatch/\'>python-stopwatch</a>, which adds static typing and a few other things.</p>\n</div>\n\n<!-- ================ BADGES/LINKS ================ -->\n\n<div align=\'center\' width=\'50%\'>\n    <h3> → STATUS ←</h3>\n    <a href="https://pepy.tech/project/python-stopwatch2">\n        <img alt="Pypi Version" src=\'https://img.shields.io/pypi/v/python-stopwatch2?&style=for-the-badge\'/>\n    </a>\n    <a href="https://www.python.org">\n        <img alt="Python Versions" src=\'https://img.shields.io/pypi/pyversions/python-stopwatch2?&style=for-the-badge\'/>\n    </a>\n    <a href="https://github.com/devRMA/python-stopwatch2">\n        <img alt="Repo Size" src=\'https://img.shields.io/github/repo-size/devRMA/python-stopwatch2?&style=for-the-badge\'/>\n    </a>\n    <a href="https://github.com/devRMA/python-stopwatch2/blob/main/LICENSE">\n        <img alt="License" src=\'https://img.shields.io/github/license/devRMA/python-stopwatch2?&style=for-the-badge\'/>\n    </a>\n    <a href="https://github.com/devRMA/python-stopwatch2/stargazers">\n        <img alt="Stars" src=\'https://img.shields.io/github/stars/devRMA/python-stopwatch2?&style=for-the-badge\'/>\n    </a>\n    <a href="https://github.com/devRMA/python-stopwatch2/graphs/contributors">\n        <img alt="Contributors" src=\'https://img.shields.io/github/contributors/devRMA/python-stopwatch2?&style=for-the-badge\'/>\n    </a>\n</div>\n\n<hr>\n\n<div align=\'center\' width=\'50%\'>\n    <a href="https://github.com/devRMA/python-stopwatch2">\n        <img alt="Tests" src=\'https://github.com/devRMA/python-stopwatch2/actions/workflows/tests.yml/badge.svg?&style=for-the-badge\'/>\n    </a>\n    <a href="https://pepy.tech/project/python-stopwatch2">\n        <img alt="Pypi Downloads" src=\'https://pepy.tech/badge/python-stopwatch2?&style=for-the-badge\'/>\n    </a>\n    <a href="https://coveralls.io/github/devRMA/python-stopwatch2">\n        <img alt="Coverage Status" src=\'https://coveralls.io/repos/github/devRMA/python-stopwatch2/badge.svg?&style=for-the-badge\'/>\n    </a>\n</div>\n\n<!-- ================ INTRODUCTION ================ -->\n<div align=\'center\'>\n    <h3>→ USAGE ←</h3>\n</div>\n\n<h3>☍ INSTALLATION</h3>\n\nTo install the library, you can just run the following command:\n\n```shell\npoetry add python-stopwatch2\n```\n\nOr, using pip:\n\n```shell\npip install python-stopwatch2\n```\n\n<h3>☍ BASIC USAGE</h3>\n\n<p><b>ƒ stopwatch.Stopwatch</b></p>\n\nYou can use the [start()](https://stopwatch2.vercel.app/api/stopwatch.html#start) and [stop()](https://stopwatch2.vercel.app/api/stopwatch.html#stop) methods to starts or stops the stopwatch counter.\n\n```python\nfrom time import sleep\n\nfrom stopwatch import Stopwatch\n\nmy_stopwatch = Stopwatch()\nsleep(2)\nmy_stopwatch.stop()\nprint(my_stopwatch.elapsed)  # 2.0\nsleep(1)\nprint(my_stopwatch.elapsed)  # 2.0\nmy_stopwatch.start()\nsleep(1)\nmy_stopwatch.stop()\nprint(my_stopwatch.elapsed)  # 3.0\nprint(f\'Time elapsed: {my_stopwatch}\')  # Time elapsed: 3.00s\n```\n\nIt is also possible to use [Stopwatch](https://stopwatch2.vercel.app/api/stopwatch.html#stopwatch) with the [with statement](https://www.geeksforgeeks.org/with-statement-in-python/).\n\n```python\nfrom time import sleep\n\nfrom stopwatch import Stopwatch\n\nwith Stopwatch() as my_stopwatch:\n    sleep(3)\nprint(my_stopwatch.elapsed)  # 3.0\nprint(f\'Time elapsed: {my_stopwatch}\')  # Time elapsed: 3.00s\n```\n<h3>☍ DOCUMENTATION</h3>\n\nTo check out the docs, visit [https://stopwatch2.vercel.app/](https://stopwatch2.vercel.app/)\n\n<h3>☍ CHANGELOG</h3>\n\nDetailed changes for each release are documented in the [CHANGELOG.md](/CHANGELOG.md).\n\n<h3>CONTRIBUTING</h3>\n\nPull requests are welcome!\n\n<h3>☍ 📑 LICENSE</h3>\n\n[MIT](https://opensource.org/licenses/MIT)\n\nCopyright (c) 2021-2022 Jonghwan Hyeon, 2022-present Rafael\n',
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
