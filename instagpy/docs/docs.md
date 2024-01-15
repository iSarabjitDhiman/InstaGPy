<h1 align="center">Documentation</h1>

## Import & Initialize.

```python
from instagpy import InstaGPy
from instagpy import config # if want to change configurations.Check out config docs.

insta = InstaGPy(use_mutiple_account=False, session_ids=None, min_requests=None, max_requests=None, timeout=None)


    """
        Args:
            use_mutiple_account (bool, optional): Set to True if want to scrape data with mutiple account sessions So that you don't get blocked. Defaults to False.
            session_ids (list, optional): List of Session IDs from Cookies. Applicable only if use_mutiple_accounts is True. Defaults to False.
            min_requests (int, optional): Minimum requests to make before shuffling a session ID. Defaults to None.
            max_requests (int, optional): Maximum requests to make before shuffling a session ID. Defaults to None.
            timeout (int, optional): Request timeout. Defaults to None.
    """
```

> ### Example - Get Basic User Details of a User.

```python
from instagpy import InstaGPy
from instagpy import config

config.PROXY = {"http":"127.0.0.1","https":"127.0.0.1"}
config.TIMEOUT = 10

insta = InstaGPy()

insta.get_user_basic_details('champagnepapi', print_formatted=True)

```
> ### Example - Get User Followers (Pagination Usage).

```python
import time, random
from instagpy import InstaGPy
from instagpy import config

config.PROXY = {"http":"127.0.0.1","https":"127.0.0.1"}
config.TIMEOUT = 10

insta = InstaGPy()

followers = []
has_more = True
cursor = None
while has_more:
    try:
        response = None
        response = insta.get_user_friends('zuck', followers_list=True, end_cursor=cursor, pagination=False)
        followers.extend(response['data'])
        has_more = response.get('has_next_page')
        if has_more:
            cursor = response.get('end_cursor')
        ## YOUR CUSTOM CODE HERE (DATA HANDLING, REQUEST DELAYS, SESSION SHUFFLING ETC.)
        ## time.sleep(random.uniform(7,10))
    except Exception as error:
        print(error)
        break


```

## Check If User is Logged In.

```python
self.logged_in

    """
        Check if user is logged in.

        Returns:
            bool: Returns True if user is logged in.
    """
```

## Log Into an Account.

```python
login(username=None, password=None, show_saved_sessions=False, save_session=True):

    """
        Login Into a user account for Data Scraping Purpose.

        Args:
            username (str, optional): Instgram Username or Email. Defaults to None.
            password (str, optional): Password. Defaults to None.
            show_saved_sessions (bool, optional): Shows saved sessions before logging into new account. Defaults to False.
            save_session (bool, optional): Save session if want to use it without logging in manually each time. Defaults to True.

        Returns:
            dict: Response from server whether got logged in.
    """
```

## Manually Generate Session with a Session ID

```python
generate_session(session_id=None):
    """
        Generates Required Headers and Cookies. OR Generates Session from an existing Session ID.

        Args:
            session_id (str, optional): Session Id from Instagram Session Cookies. Defaults to None.
    """
```

## Shuffle Session Manually.

```python
shuffle_session(ignore_requests_limit=False):

    """
        Shuffle session/cookies. Takes a new session ID from self.session_ids only if using with mutiple accounts.

        Args:
            ignore_requests_limit (bool, optional): Set to True to shuffle session manually regardless of min/max number of requests. Defaults to False.

        Returns:
            Session object: Session Object i.e. self.session
    """
```

## Get Session ID.

```python
get_session_id(username=None, password=None, new_session=False)

    """
        Get sessionID of the current session OR a new login session. By default returns current one if logged in.

        Args:
            username (str): Username OR Email. Defaults to None
            password (str): Password. Defaults to None
            new_session (bool, optional): Set to True if want to get session ID from a new session. Otherwise It will return the already logged In session ID. Defaults to False.

        Returns:
            str: Session ID.
    """
```

## Get Logged In User Details.

```python
self.me

    """
        Returns Logged in User Information.

        Returns:
            dict: Currently logged in User Data.
    """
```

## Get User ID of a User.

```python
get_user_id(username)
```

## Get a brief overview of a user.

```python
get_user_basic_details(username, print_formatted=False)

    """
        Get a brief overview of an Instagram Profile.

        Args:
            username (str, optional): Instagram Username. Defaults to None.
            print_formatted (bool, optional): Print Data in a Structure way. Defaults to False.

        Returns:
            dict: User Data.
    """
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
get_user_data(user_id)
#if username is given, it will automatically be converted to user_id.
#so works with both username and user_id. but will make an additional request to get user_id.
    """
        Extracts user details. With Contact Info Like email, phone and address.

        Args:
            user_id (int): User ID of an Instagram User.

        Returns:
            dict: user info along with contact info.
    """
        # returns almost as same data as get_user_info method Except this one returns contact info (email/phone) as well. |LOGIN REQUIRED|
```

## Get User About Info (location, if running any ads, verified, Joining Date, Verification Date). -- LOGIN REQUIRED

```python
get_about_user(username, print_formatted=True)

    """
        Returns user about details like account location, if running any ads, verified, Joining Date, Verification Date.

        Args:
            username (str): Username of the person
            print_formatted (bool, optional): Returns only necessary and structure data if set to True Else would return the whole dataset. Defaults to True.

        Returns:
            dict: User About Dataset.
    """
```

## Get Followers OR Followings List of a User. -- LOGIN REQUIRED

```python
get_user_friends(username, followers_list=False, followings_list=False, end_cursor=None, total=None, pagination=True)

    """
        Fetch follower or following list of a user.

        Args:
            username (str): Instagram Username.
            followers_list (bool, optional): Set True if want to extract user's followers list. Defaults to False.
            followings_list (bool, optional): Set True if want to extract user's followings list. Defaults to False.
            end_cursor (str, optional): Last endcursor point. (To start from where you left off last time). Defaults to None.
            total (int, optional): Total number of results to extract. Defaults to None. -- Gets all by default.
            pagination (bool, optional): Set to False if want to handle each page request manually. Use end_cursor from the previous page/request to navigate to the next page. Defaults to True.

        Returns:
            dict: Returns data, end_cursor, has_next_page
    """
```

## Get All Profile Media from a User Profile.

```python
get_profile_media(username, end_cursor=None, from_date=None, to_date=None, total=None, pagination=True)

    """
        Returns all media/posts of the given Instagram Profile.

        Args:
            username (str): Instagram Username.
            end_cursor (str, optional): Last endcursor point. (To start from where you left off last time). Defaults to None.
            from_date (str, optional): FORMAT - 'Year-Month-Date' Fetch posts starting from a specified period of time. Defaults to None.
            to_date (str, optional): FORMAT - 'Year-Month-Date'  Fetch posts upto a specified period of time. Defaults to None.
            total (int, optional): Total number of results to extract. Defaults to None. -- Gets all by default.
            pagination (bool, optional): Set to False if want to handle each page request manually. Use end_cursor from the previous page/request to navigate to the next page. Defaults to True.

        Returns:
            dict: Returns data, end_cursor, has_next_page
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

## Get Media Posts from a Hashtag. -- LOGIN REQUIRED

```python
get_hashtag_posts(hashtag=None, end_cursor=None, total=None, pagination=True)

    """
        Get media posts from hashtags.

        Args:
            hashtag (str): Hashtag that you want to extract data from. Accepts both formats i.e. hashtag or #hashtag. Defaults to None.
            end_cursor (str, optional): Last endcursor point. (To start from where you left off last time). Defaults to None.
            total (int, optional): Total number of results to extract. Defaults to None. -- Gets all by default.
            pagination (bool, optional): Set to False if want to handle each page request manually. Use end_cursor from the previous page/request to navigate to the next page. Defaults to True.

        Returns:
            dict: Returns data, end_cursor, has_next_page
    """
```
