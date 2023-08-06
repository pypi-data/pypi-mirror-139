# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['steamwine']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8.1,<4.0.0']

setup_kwargs = {
    'name': 'steamwine',
    'version': '0.0.1',
    'description': 'Simple work with API Steam',
    'long_description': '# steamwine\nExample:\n\n\n```py\nimport asyncio\nfrom steamwine import Steam\n\napi = Steam("API_KEY")\n\n\nasync def handler():\n\tfriends = await api.user.friends(76561198982570889)\n\n\tfor friend in friends.friends_list:\n\t\tusr = await api.user.get(friend.steam_id)\n\t\tprint(usr.players[0].name)\n\n\nasyncio.get_event_loop().run_until_complete(handler())\n```\n',
    'author': 'Fsoky',
    'author_email': 'cyberuest0x12@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Fsoky/steamwine',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
