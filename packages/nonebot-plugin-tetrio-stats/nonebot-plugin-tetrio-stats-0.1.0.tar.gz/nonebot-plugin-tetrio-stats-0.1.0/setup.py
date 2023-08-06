# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot-plugin-tetrio-stats']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8.1,<4.0.0', 'asyncio>=3.4.3,<4.0.0']

setup_kwargs = {
    'name': 'nonebot-plugin-tetrio-stats',
    'version': '0.1.0',
    'description': '一个在nonebot2中查询TRTRIO玩家数据的插件，同时支持绑定TRTRIO账号',
    'long_description': 'TETRIO Stats\n===\n* 它能做什么？\n  - 通过访问 [TETR.IO](https://ch.tetr.io)的API 来获取游戏统计信息。\n  - 通过群内指令`iobind`来绑定自己的账号。\n* 指令列表\n| 指令 | 说明 |\n| --- | --- |\n| `io查USERID` | 查询游戏统计信息 |\n| `iobind` | 绑定自己的账号 |',
    'author': 'scdhh',
    'author_email': 'wallfjjd@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
