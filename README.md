<h1 align="center">InstaGPy</h1>

<p align="center">
<a href="https://choosealicense.com/licenses/mit/"> <img src="https://img.shields.io/badge/License-MIT-green.svg"></a>
<a href="https://www.python.org/"><img src="https://img.shields.io/pypi/pyversions/instagpy"></a>
<a href="https://pypi.org/project/instagpy/"> <img src="https://img.shields.io/pypi/v/instagpy"></a>
<a href="https://github.com/iSarabjitDhiman/InstaGPy/commits"> <img src="https://img.shields.io/github/last-commit/iSarabjitDhiman/InstaGPy"></a>
<a href="https://twitter.com/isarabjitdhiman"> <img src="https://img.shields.io/twitter/follow/iSarabjitDhiman?style=social"></a>

## Overview

InstaGPy is an Instagram Unofficial API to extract data from Instargam Profiles. Scrape data from user's profile like username, userid, bio, email, phone, followers/followings list, profile media, account_type, etc.

> _Note_ : `Use it on Your Own Risk. Scraping with Residential proxies is advisable while extracting data at scale/in bulk. If possible, use multiple accounts to fetch data from Instagram.` **_DON'T USE YOUR PERSONAL ACCOUNT FOR SCRAPING PURPOSES._**

## Installation

Install InstaGPy with pip

```python
  pip install instagpy
```

## Usage/Examples

```python
python quickstart.py
```

OR

```python
from instagpy import InstaGPy

InstaGPy(use_mutiple_account=False, session_ids=None, min_requests=None, max_requests=None)
```

> ### Example - Get Basic User Details of a User

```python
from instagpy import InstaGPy

insta = InstaGPy()

insta.get_user_basic_details('champagnepapi',pretty_print=True)

```

## Documentation

Check out step by step guide.

[Documentation](instagpy/docs/docs.md)

## Configuration

> ### Example - Config Usage

```python
from instagpy import config

config.PROXY = {"http":"127.0.0.1","https":"127.0.0.1"}
config.TIMEOUT = 10

```

Check out configuration docs for the available settings.

[Configurations](instagpy/docs/config.md)

## Features

- Extracts User's Followers
- Extracts User's Followings
- Extracts User's Profile Details along with Contact Details (Phone, WhatsApp, Email & Address)
- Extracts Instagram Profile Media

## Authors

- [@iSarabjitDhiman](https://www.github.com/iSarabjitDhiman)

## Feedback

If you have any feedback, please reach out to us at hello@sarabjitdhiman.com or contact me on Social Media @iSarabjitDhiman

## Support

For support, email hello@sarabjitdhiman.com
