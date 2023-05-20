<h1 align="center">Documentation</h1>

## Import & Initialize.

```python
from instagpy import InstaGPy

insta = InstaGPy(max_retries=None, proxies=None, use_mutiple_account=False, session_ids=None, min_requests=None, max_requests=None)


    """
        Args:
            max_retries (int, optional): Number of retires for each request. Defaults to None.
            proxies (dict, optional): Proxies as a dictionary {'http': proxy_here,'https':proxy_here}. Residential Proxies are recommended. Defaults to None.
            use_mutiple_account (bool, optional): Set to True if want to scrape data with mutiple account sessions So that you don't get blocked. Defaults to False.
            session_ids (list, optional): List of Session IDs from Cookies. Applicable only if use_mutiple_accounts is True. Defaults to False.
            min_requests (int, optional): Minimum requests to make before shuffling a session ID. Defaults to None.
            max_requests (int, optional): Maximum requests to make before shuffling a session ID. Defaults to None.
    """
```

> ### Example - Get Basic User Details of a User.

```python
from instagpy import InstaGPy

insta = InstaGPy()

print(insta.get_user_basic_details('champagnepapi'))

```

## Check If User is Logged In.

```python
logged_in()

    """
        Check if user is logged in.

        Returns:
            bool: Returns True if user is logged in.
    """
```

## Log Into an Account.

```python
login(username=None, password=None, show_saved_sessions=True, save_session=True):

    """
        Login Into a user account for Data Scraping Purpose.

        Args:
            username (str, optional): Instgram Username or Email. Defaults to None.
            password (str, optional): Password. Defaults to None.
            show_saved_sessions (bool, optional): Shows saved sessions before logging into new account. Defaults to True.
            save_session (bool, optional): Save session if want to use it without logging in manually each time. Defaults to True.

        Returns:
            dict: Response from server whether got logged in.
    """
```

## Get User ID of a User.

```python
get_user_id(username)
```

## Get User Details i.e. userid, username, bio, friends count etc.

```python
get_user_info(username)

    """
        Extracts user details.

        Args:
            username (str): Instagram username.

        Returns:
            dict: user info like username,id,bio,follower/following count etc.
    """
```

## Get User Details with contact Info i.e. phone, email, whatsapp no., address etc. -- LOGIN REQUIRED

```python
get_user_info(username)

    """
        Extracts user details. With Contact Info Like email, phone and address.

        Args:
            user_id (int): User ID of an Instagram User.

        Returns:
            dict: user info along with contact info.
    """
        # returns almost as same data as get_user_info method Except this one returns contact info (email/phone) as well. |LOGIN REQUIRED|
```

## Get a brief overview of a user.

```python
get_user_basic_details(username)

    """
        Check if user is logged in.

        Returns:
            bool: Returns True if user is logged in.
    """
```

## Get Followers OR Followings List of a User. -- LOGIN REQUIRED

```python
get_user_friends(username, followers_list=False, followings_list=False, end_cursor=None, max=None)

    """
        Fetch follower or following list of a user.

        Args:
            username (str): Instagram Username.
            followers_list (bool, optional): Set True if want to extract user's followers list. Defaults to False.
            followings_list (bool, optional): Set True if want to extract user's followings list. Defaults to False.
            end_cursor (str, optional): Last endcursor point. (To start from where you left off last time). Defaults to None.
            max (int, optional): Number of results per request to extract from Instagram Database. Defaults to None.

        Returns:
            list: All followers or followings.
    """
```

## Get All Profile Media from a User Profile.

```python
get_profile_media(username, end_cursor=None, from_date=None, to_date=None, max=None)

    """
        Returns all media/posts of the given Instagram Profile.

        Args:
            username (str): Instagram Username.
            end_cursor (str, optional): Last endcursor point. (To start from where you left off last time). Defaults to None.
            from_date (str, optional): FORMAT - 'Year-Month-Date' Fetch posts starting from a specified period of time. Defaults to None.
            to_date (str, optional): FORMAT - 'Year-Month-Date'  Fetch posts upto a specified period of time. Defaults to None.
            max (int, optional): Number of results per request to extract from Instagram Database. Defaults to None.

        Returns:
            list: All Posts of the given Instagram user.
    """
```

## Get Post Details of a Particular Media Post. i.e. publish time, caption, url etc.

```python
get_post_details(post_url)

    """
        Get details of a particular Instagram Post/Media.

        Args:
            post_url (str): Instagram Post/Picture/Reel URL.

        Returns:
            dict: All the details like post_id,datetime,caption,url,location etc.
    """
```

## Get Media URL for downloading Purpose.

```python
get_media_url(response)

    """
        Extracts High Resolution/Quality Media URL from post details response returned from get_post_details method.

        Args:
            response (dict): Response returned from get_post_details method.

        Returns:
            list/str: Returns List if carousel Else string its a video or a single picture.
    """
```
