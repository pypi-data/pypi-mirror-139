# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot_plugin_everyday_en']

package_data = \
{'': ['*']}

install_requires = \
['aiofiles>=0.7.0,<0.8.0',
 'httpx>=0.22.0,<0.23.0',
 'nonebot-adapter-onebot>=2.0.0-beta.1,<3.0.0',
 'nonebot2>=2.0.0-beta.1,<3.0.0']

setup_kwargs = {
    'name': 'nonebot-plugin-everyday-en',
    'version': '1.1.2',
    'description': '每日一句英文句子。完整帮助文档，可选搭配软依赖nonebot_plugin_apscheduler实现定时发送',
    'long_description': None,
    'author': 'MelodyYuuka',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
