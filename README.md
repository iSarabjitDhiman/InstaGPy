<h1 align="center">InstaGPy</h1>

<center>

[![MIT license](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)
![GitHub release (latest by date)](https://img.shields.io/github/v/release/iSarabjitDhiman/InstaGPy)
![GitHub Release Date](https://img.shields.io/github/release-date/iSarabjitDhiman/InstaGPy)
![GitHub last commit](https://img.shields.io/github/last-commit/iSarabjitDhiman/InstaGPy)
![Twitter Follow](https://img.shields.io/twitter/follow/iSarabjitDhiman?style=social)

</center>

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

InstaGPy(proxies=proxies, max_requests=3, use_mutiple_account=False, session_ids=None, min_requests=None, max_retries=None)
```

> ### Example - Get Basic User Details of a User

```python
from instagpy import InstaGPy

insta = InstaGPy()

print(insta.get_user_basic_details('champagnepapi'))

```

## Documentation

Check out step by step guide.

[Documentation](instagpy/docs/docs.md)

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
