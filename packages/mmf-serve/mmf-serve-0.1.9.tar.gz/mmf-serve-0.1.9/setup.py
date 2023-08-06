# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mmf_serve']

package_data = \
{'': ['*']}

install_requires = \
['PyTurboJPEG>=1,<2',
 'aiofile>=3,<4',
 'cryptography>=36',
 'mmf-meta[all]>=0.1.13,<0.2.0',
 'orjson>=3,<4',
 'pydantic[dotenv]>=1.9,<2.0',
 'requests>=2,<3']

extras_require = \
{'fastapi': ['fastapi>=0.64,<1.0'], 'python-multipart': ['fastapi>=0.64,<1.0']}

entry_points = \
{'console_scripts': ['mmfserve = mmf_serve:cli']}

setup_kwargs = {
    'name': 'mmf-serve',
    'version': '0.1.9',
    'description': 'Часть проекта MMF отвечающая за serving',
    'long_description': '# MMF-meta\nЭта библиотека - часть проекта Model Management Framework.\n\nОтвечает за serving\n\n### Пример использования\n```shell\nmmfserve serve-rabbit\n```\n\nКонфигурация\n```dotenv\nRABBIT__USER=core\nRABBIT__PASSWORD=somesecret\nRABBIT__HOST=localhost\nEXCHANGE_NAME=test_exchange\nQUEUE_NAME=test_queue\nMAIN_SCRIPT=main.py\n```\n[Подробная документация](https://mm-framework.github.io/docs/)\n',
    'author': 'Викторов Андрей Германович',
    'author_email': 'andvikt@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
