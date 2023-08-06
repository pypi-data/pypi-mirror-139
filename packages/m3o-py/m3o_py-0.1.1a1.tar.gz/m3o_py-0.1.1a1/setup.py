# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['m3o_py']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8.1,<4.0.0', 'pydantic>=1.9.0,<2.0.0']

extras_require = \
{'aiodns': ['aiodns>=3.0.0,<4.0.0']}

setup_kwargs = {
    'name': 'm3o-py',
    'version': '0.1.1a1',
    'description': 'Python-library for M3O',
    'long_description': "# M3O-Py\n\nThis is the python library for [M3O](https://github.com/m3o/m3o).\n\n## Installation\n\n1. Install pipenv: `pip install poetry`\n2. Clone the repo: `git clone https://github.com/mawoka-myblock/m3o-py`\n3. Install the dependencies: `poetry install`\n\n### Run the tests\n\n1. Set your environment variables: `export M3O_API_KEY=<your_api_key>`\n2. Run the tests: `poetry run pytest tests --asyncio-mode=strict`\n\n## Supported API's\n\n- [x] [Cache](https://m3o.com/cache) Coverage: 75%\n- [x] [Contacts](https://m3o.com/contact) Coverage: 90%\n- [x] [Database](https://m3o.com/db) Coverage: 75%\n- [x] [Answers](https://m3o.com/answer) Coverage: 95%\n- [x] [Jokes](https://m3o.com/joke) Coverage: 92%\n- [x] [Address](https://m3o.com/address) **NO TEST SINCE IT'S NOT FREE**\n- [x] [IDgen](https://m3o.com/id) Coverage: 90%\n- [x] [IP2Geo](https://m3o.com/ip) Coverage: 96%\n- [x] [Twitter](https://m3o.com/twitter) Coverage: 92%\n- [x] [Weather](https://m3o.com/weather) Coverage: 97%\n- [ ] [Apps](https://m3o.com/app)\n- [ ] [Avatar](https://m3o.com/avatar)\n- [ ] [Carbon](https://m3o.com/carbon)\n- [ ] [Chat](https://m3o.com/chat)\n- [ ] [Comments](https://m3o.com/comments)\n- [ ] [Crypto](https://m3o.com/crypto)\n- [ ] [Currency](https://m3o.com/currency)\n- [ ] [Email](https://m3o.com/email)\n- [ ] [Emoji](https://m3o.com/emoji)\n- [ ] [EV Chargers](https://m3o.com/evchargers)\n- [ ] [Events](https://m3o.com/event)\n- [ ] [Files](https://m3o.com/file)\n- [ ] [Forex](https://m3o.com/forex)\n- [ ] [Functions](https://m3o.com/function)\n- [ ] [Geocoding](https://m3o.com/geocoding)\n- [ ] [GIFs](https://m3o.com/gifs)\n- [ ] [Goole](https://m3o.com/google)\n- [ ] [Hello World](https://m3o.com/helloworld)\n- [ ] [Holidays](https://m3o.com/holidays)\n- [ ] [Image](https://m3o.com/image)\n- [ ] [Lists](https://m3o.com/lists)\n- [ ] [Location](https://m3o.com/location)\n- [ ] [Meme Generator](https://m3o.com/memegen)\n- [ ] [Minecraft](https://m3o.com/minecraft)\n- [ ] [Movies](https://m3o.com/movie)\n- [ ] [Message Queue](https://m3o.com/mq)\n- [ ] [News](https://m3o.com/news)\n- [ ] [NFTs](https://m3o.com/nft)\n- [ ] [Notes](https://m3o.com/notes)\n- [ ] [OTP](https://m3o.com/otp)\n- [ ] [Ping](https://m3o.com/ping)\n- [ ] [Places](https://m3o.com/place)\n- [ ] [Postcode](https://m3o.com/postcode)\n- [ ] [Prayer](https://m3o.com/prayer)\n- [ ] [QR Codes](https://m3o.com/qr)\n- [ ] [Quran](https://m3o.com/quran)\n- [ ] [Routes](https://m3o.com/routing)\n- [ ] [RSS](https://m3o.com/rss)\n- [ ] [Search](https://m3o.com/search)\n- [ ] [Sentiment](https://m3o.com/sentiment)\n- [ ] [SMS](https://m3o.com/sms)\n- [ ] [Space](https://m3o.com/space)\n- [ ] [Spam](https://m3o.com/spam)\n- [ ] [Stocks](https://m3o.com/stock)\n- [ ] [Stream](https://m3o.com/stream)\n- [ ] [Sunnah](https://m3o.com/sunnah)\n- [ ] [Thumbnail](https://m3o.com/thumbnail)\n- [ ] [Time](https://m3o.com/time)\n- [ ] [Translate](https://m3o.com/translate)\n- [ ] [URLs](https://m3o.com/url)\n- [ ] [Users](https://m3o.com/user)\n- [ ] [Vehicle](https://m3o.com/vehicle)\n- [ ] [YouTube](https://m3o.com/youtube)",
    'author': 'Mawoka',
    'author_email': 'mawoka-myblock@e.email',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mawoka-myblock/m3o-py',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
