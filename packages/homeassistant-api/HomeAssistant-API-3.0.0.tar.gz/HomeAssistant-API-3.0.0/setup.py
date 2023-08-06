# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['homeassistant_api',
 'homeassistant_api._async',
 'homeassistant_api._async.models',
 'homeassistant_api.models']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp-client-cache>=0.6.1,<0.7.0',
 'aiohttp>=3.8.1,<4.0.0',
 'pydantic>=1.9.0,<2.0.0',
 'requests-cache>=0.9.2,<0.10.0',
 'requests>=2.26.0,<3.0.0',
 'simplejson>=3.17.6,<4.0.0']

setup_kwargs = {
    'name': 'homeassistant-api',
    'version': '3.0.0',
    'description': "Python Wrapper for Homeassistant's REST API",
    'long_description': '# HomeassistantAPI\n\n![Lines of code](https://img.shields.io/tokei/lines/github/GrandMoff100/HomeassistantAPI?style=for-the-badge)\n![PyPI - Downloads](https://img.shields.io/pypi/dm/HomeAssistant-API?style=for-the-badge)\n![GitHub commits since latest release (by date including pre-releases)](https://img.shields.io/github/commits-since/GrandMoff100/HomeassistantAPI/latest/dev?include_prereleases&style=for-the-badge)\n![Read the Docs (version)](https://img.shields.io/readthedocs/homeassistantapi/stable?style=for-the-badge)\n![GitHub release (latest by date)](https://img.shields.io/github/v/release/GrandMoff100/HomeassistantAPI?style=for-the-badge)\n![GitHub release (latest by date)](https://img.shields.io/github/downloads/GrandMoff100/HomeassistantAPI/latest/total?style=for-the-badge)\n\n![Home AssistantLogo](https://github.com/GrandMoff100/HomeAssistantAPI/blob/7edb4e6298d37bda19c08b807613c6d351788491/docs/images/homeassistant-logo.png?raw=true)\n\nPython Wrapper for Homeassistant\'s [REST API](https://developers.home-assistant.io/docs/api/rest/)\n\n\nPlease ⭐️ the repo if you find this project useful or cool!\n\nHere is a quick example.\n```py\nfrom homeassistant_api import Client\n\nwith Client(\n    \'<API Server URL>\',\n    \'<Your Long Lived Access-Token>\'\n) as client:\n\n    light = client.get_domain("light")\n\n    light.turn_on(entity_id=\'light.living_room_lamp\')\n```\n\n## Documentation\nAll documentation, API reference, Contribution guidelines and pretty much everything else you\'d want to know is on our readthedocs site [here](https://homeassistantapi.readthedocs.io)\n\nIf theres something missing open an issue and let us know! Thanks!\n\nGo make some cool stuff! Maybe come back and tell us about it in a [discussion](https://github.com/GrandMoff100/HomeAssistantAPI/discussions)? We\'d love to hear about how you use our library!!\n',
    'author': 'GrandMoff100',
    'author_email': 'minecraftcrusher100@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/GrandMoff100/HomeAssistantAPI',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
