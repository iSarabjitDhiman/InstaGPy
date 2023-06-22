<h1 align="center">Configuration</h1>

# Importing

```python
from instagpy import config
```

> ### Example - Config Usage

```python
from instagpy import InstaGPy
from instagpy import config

config.PROXY = {"http":"127.0.0.1","https":"127.0.0.1"}
config.TIMEOUT = 10

insta = InstaGPy()

insta.get_user_basic_details('champagnepapi',print_formatted=True)

```

## Requests Limit for Sessions

```python
# Minimum requests to make before shuffling a session
config.MIN_REQUESTS = 3
```

```python
# Maximum requests to make before shuffling a session
config.MAX_REQUESTS = 6
```

## Retries Limit

```python
# Maximun number of retries for each request
config.MAX_RETRIES = 3
```

## Request Timeout

```python
# request timeout - in seconds
config.TIMEOUT = 5
```

## Using Proxies

```python
# Example {"http":"proxy_here","https":"proxy_here"} Accepts python dictionary.
config.PROXY = None
```

## Saved Sessions Directory

```python
# Directory to save and load logged in sessions/cookies
config.SESSION_DIRECTORY = "Insta Saved Sessions"
```
