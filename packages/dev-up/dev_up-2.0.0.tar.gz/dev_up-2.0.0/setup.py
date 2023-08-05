# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dev_up',
 'dev_up.abc',
 'dev_up.base',
 'dev_up.categories',
 'dev_up.models',
 'dev_up.models.request',
 'dev_up.models.request.audio',
 'dev_up.models.request.profile',
 'dev_up.models.request.utils',
 'dev_up.models.request.vk',
 'dev_up.models.response',
 'dev_up.models.response.audio',
 'dev_up.models.response.profile',
 'dev_up.models.response.utils',
 'dev_up.models.response.vk']

package_data = \
{'': ['*']}

install_requires = \
['Pygments>=2.10.0,<3.0.0',
 'aiohttp>=3.8.1,<4.0.0',
 'cachetools>=4.2.4,<5.0.0',
 'loguru>=0.5.3,<0.6.0',
 'pydantic>=1.8.2,<2.0.0',
 'requests>=2.26.0,<3.0.0',
 'update>=0.0.1,<0.0.2']

setup_kwargs = {
    'name': 'dev-up',
    'version': '2.0.0',
    'description': 'Библиотека для работы с сервисом DEV-UP.',
    'long_description': '# DEV UP API wrapper\n\n![PyPI](https://img.shields.io/pypi/v/dev-up)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/dev-up)\n![GitHub](https://img.shields.io/github/license/lordralinc/dev_up)\n[![Downloads](https://pepy.tech/badge/dev-up)](https://pepy.tech/project/dev-up)\n## Установка \n```shell\npip install dev_up\n```\n\n\n\n## Получение токена\n[dev-up.ru](https://dev-up.ru/lk)\n\n## Использование\n\n```python\nfrom dev_up import DevUpAPI\n\napi = DevUpAPI("token")\nprofile = await api.profile.get()\nstickers = await api.vk.get_stickers(1)\n\ncustom = await api.make_request(\n    "section.method",\n    data=dict(param1="foo", param2="bar")\n)\n```',
    'author': 'lordralinc',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/lordralinc/dev_up',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>3.7,<4.0',
}


setup(**setup_kwargs)
