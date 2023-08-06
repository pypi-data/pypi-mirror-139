# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot-plugin-tetrio-stats']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8.1,<4.0.0',
 'asyncio>=3.4.3,<4.0.0',
 'nonebot-adapter-onebot>=2.0.0-beta.1,<3.0.0',
 'nonebot2>=2.0.0-beta.2,<3.0.0',
 'repository']

setup_kwargs = {
    'name': 'nonebot-plugin-tetrio-stats',
    'version': '0.2.0',
    'description': '一个在nonebot2中查询TETRIO玩家数据的插件，同时支持绑定TETRIO账号',
    'long_description': 'TETRIO Stats\n===\n一个在nonebot2中查询TETRIO玩家数据的插件，同时支持绑定TETRIO账号\n\n安装\n---\n* 使用 pip\n```\npip install nonebot-plugin-tetrio-stats\n```\n使用\n---\n参考NoneBot2文档 [加载插件](https://v2.nonebot.dev/docs/tutorial/plugin/load-plugin/)\n\n依赖\n---\n目前只支持 `OneBot V11` 协议\n\n指令列表\n---\n\n | 指令 | 说明 |\n | --------- | --------- |\n | io查`USERID` | 查询游戏统计信息 |\n | iobind`USERID` | 绑定自己的账号 |\n\n鸣谢\n---\n* [NoneBot2](https://v2.nonebot.dev/)\n* [OneBot](https://onebot.dev/)\n* [TETR.IO](https://tetr.io/)\n\n开源\n---\n本项目使用[MIT](https://github.com/shoucandanghehe/nonebot-plugin-tetrio-stats/blob/main/LICENSE)许可证开源',
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
