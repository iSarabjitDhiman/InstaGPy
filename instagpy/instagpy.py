import requests
import json
import datetime
import time
import getpass
import random
# custom
from . import config
from . import session_util
from . import utils
from . import path
from .request_util import make_request
from functools import reduce


class InstaGPy:

    def __init__(self, use_mutiple_account=False, session_ids=None, min_requests=None, max_requests=None):
        """

        Args:
            use_mutiple_account (bool, optional): Set to True if want to scrape data with mutiple account sessions So that you don't get blocked. Defaults to False.
            session_ids (list, optional): List of Session IDs from Cookies. Applicable only if use_mutiple_accounts is True. Defaults to False.
            min_requests (int, optional): Minimum requests to make before shuffling a session ID. Defaults to None.
            max_requests (int, optional): Maximum requests to make before shuffling a session ID. Defaults to None.
            timeout (int, optional): Request timeout. Defaults to None.
        """
        if use_mutiple_account and not session_ids:
            raise Exception(
                'Either Pass a list of session_ids or set use_multiple_account to False.')
        if use_mutiple_account and session_ids:
            self.current_request_number = 1
            # shuffle session randomly after every nth request.
            self.min_requests = min_requests or config.MIN_REQUESTS
            self.max_requests = max_requests or config.MAX_REQUESTS
            self.shuffle_session_after = random.randint(
                self.min_requests, self.max_requests)
            self.session_ids_container = None
        self.session_ids = session_ids
        self.use_mutiple_account = use_mutiple_account
        self.generate_session()

    @property
    def me(self):
        """Returns Logged in User Information.

        Returns:
            dict: Currently logged in User Data.
        """
        response = self._get_meta_data()
        return response.get('config', {}).get('viewer', None)

    def _get_meta_data(self):
        """Returns Browser's and User's Meta Data.

        Returns:
            dict: Meta Data.
        """
        response = make_request(path.META_DATA_URL)
        return response
    
    def login_decorator(original_function):
        def wrapper(self, *args, **kwargs):
            if not self.logged_in:
                self.login()
            return original_function(self, *args, **kwargs)
        return wrapper

    def generate_session(self, session_id=None):
        """Generates Required Headers and Cookies. OR Generates Session from an existing Session ID.

        Args:
            session_id (str, optional): Session Id from Instagram Session Cookies. Defaults to None.
        """
        self.session = requests.Session()
        if config.PROXY is not None:
            self.session.proxies = config.PROXY
            self.session.verify = False
        self.session.headers.update(
            {"User-Agent": random.choice(config._USER_AGENTS)})
        make_request(path.BASE_URL, session=self.session)
        response = requests.get(path.LOGIN_URL)
        for _ in range(config.MAX_RETRIES):
            if response.cookies:
                break
            response = self.session.get(path.LOGIN_URL)
        csrf_token = dict(response.cookies).get("csrftoken",None)
        if not csrf_token:
            raise Exception("Couldn't generate CSRF Token")
        self.session.headers.update(
            {'x-csrftoken': csrf_token, 'X-Requested-With': "XMLHttpRequest", 'Referer': path.BASE_URL})
        self.session.cookies = response.cookies
        if session_id:
            # load an existing session with session_id
            self.session.cookies.update({'sessionid': session_id})

        try:
            self.me
        except:
            pass
        config._DEFAULT_SESSION = self.session
        return self.session
    
    def _handle_pagination(self, data_path=None, total=None, from_date=None, to_date=None, data_count=None, request_config=None, pagination=True):
        # fmt: off  - Turns off formatting for this block of code. Just for the readability purpose.
        def filter_data(response):
            filtered_data = []
            for each_entry in response:
                if from_date or to_date:
                    created_at = datetime.datetime.fromtimestamp(each_entry.get("node",{}).get("taken_at_timestamp"))
                if from_date and created_at and created_at <= from_date:
                    continue
                if to_date and created_at and created_at >= to_date:
                    continue
                if total is not None and (len(data_container['data']) + len(filtered_data)) >= total:
                    return filtered_data
                filtered_data.append(each_entry)
            return filtered_data
        
        if not request_config or not isinstance(request_config, dict):
            raise Exception("Invalid request config")
        if not data_path:
            raise Exception("No data path specified")
        if not pagination and total:
            raise Exception("Either enable the pagination or disable total number of results.")
        data_container = {"data": [],"end_cursor": None, "has_next_page": True}
        while data_container["has_next_page"]:
            try:
                request_payload = self._generate_request_data(**request_config)
                response = make_request(**request_payload)
                data = reduce(dict.get, data_path, response)
                end_cursor = data.get("page_info",{}).get("end_cursor",None) if isinstance(data, dict) else None or response.get("next_max_id",None)
                has_next_page = data.get("page_info",{}).get("has_next_page",None) if isinstance(data, dict) else None or response.get("big_list", None)
                if not data_count:
                    data_count = data.get("count","") if isinstance(data, dict) else ""
                if isinstance(data, dict):
                    data = data.get('edges',[])
                data_container['data'].extend(filter_data(data))
                
                print(f"Fetched Data : {len(data_container['data'])} / {data_count}".strip(" /"), end="\r")

                if end_cursor:
                    request_config['end_cursor'] = end_cursor
                    data_container['end_cursor'] = end_cursor

                if not has_next_page:
                    data_container["has_next_page"] = False

                if not data_container["has_next_page"] or (total is not None and len(data_container['data']) >= total) or not pagination:
                    return data_container
                
                if from_date:
                    if any(datetime.datetime.fromtimestamp(post['node']['taken_at_timestamp']) <= from_date for post in data['edges']):
                        return data_container
                
                self.shuffle_session()
            # fmt: on 
            except ConnectionError as error:
                print(error)
                continue

            except Exception as error:
                print(error)
                return data_container

    def shuffle_session(self, ignore_requests_limit=False):
        """Shuffle session/cookies. Takes a new session ID from self.session_ids if using with mutiple accounts.

        Args:
            ignore_requests_limit (bool, optional): Set to True to shuffle session manually regardless of min/max number of requests. Defaults to False.

        Returns:
            Session object: Session Object i.e. self.session
        """
        if not self.use_mutiple_account:
            return
        change_session = False
        if ignore_requests_limit:
            change_session = True
        if not ignore_requests_limit:
            self.current_request_number += 1
            if self.current_request_number % self.shuffle_session_after == 0:
                self.shuffle_session_after = random.randint(
                    self.min_requests, self.max_requests)
                change_session = True
        if change_session:
            if not self.session_ids_container:
                self.session_ids_container = self.session_ids.copy()
            session_id = self.session_ids_container.pop()
            return self.generate_session(session_id=session_id)

    def _generate_request_data(self, url=None, query=None, count=None, user_id=None, end_cursor=None, search_surface=None, shortcode=None, hashtag=None, is_graphql=False):
        """Generates request payload for instagram api requests.

        Args:
            url (str, optional): Request URL. Defaults to None.
            query (str, optional): Query endpoint. Defaults to None.
            count (int, optional): Number of results per request to extract from Instagram Database. Defaults to None.
            user_id (int, optional): User Profile ID. Defaults to None.
            end_cursor (str, optional): Last endcursor point. (To start from where you left off last time). Defaults to None.
            search_surface (str, optional): Source of request. Defaults to None.
            shortcode (str, optional): Instagram Post ID. Defaults to None.
            is_graphql (bool, optional): If its a Graphql query or standard request. Defaults to False.

        Returns:
            dict: request payload
        """
        params = {}
        if is_graphql:
            params["query_hash"] = query
            data = {}
            if user_id:
                data['id'] = user_id
            if count:
                data['first'] = count
            if end_cursor:
                data['after'] = end_cursor
            if shortcode:
                data['shortcode'] = shortcode
            if hashtag:
                data['tag_name'] = hashtag

            params["variables"] = json.dumps(data)
        else:
            if count:
                params["count"] = count
            if search_surface is not None:
                params["search_surface"] = search_surface
            if end_cursor is not None:
                params["max_id"] = end_cursor
                
        request_payload = {"url": url or path.GRAPHQL_URL, "params": params}
        return request_payload

    def login(self, username=None, password=None, show_saved_sessions=False, save_session=True):
        """Login Into a user account for Data Scraping Purpose.

        Args:
            username (str, optional): Instgram Username or Email. Defaults to None.
            password (str, optional): Password. Defaults to None.
            show_saved_sessions (bool, optional): Shows saved sessions before logging into new account. Defaults to False.
            save_session (bool, optional): Save session if want to use it without logging in manually each time. Defaults to True.

        Returns:
            dict: Response from server whether got logged in.
        """
        if show_saved_sessions or (username is None and password is None):
            if show_saved_sessions is not False:
                session_util.load_session(session=self.session)
                return
        if username is None:
            username = str(input("Enter Your Username or Email : ")).strip()

        try:
            session_util.load_session(filename=username, session=self.session)
            user = self.me
            if not user:
                print("Restored Session has been Expired. Trying to Login...")
                raise Exception("Session Expired.")
            print(f"{user.get('full_name','')} : Session Restored.")
        except:
            self.generate_session()
            if password is None:
                password = getpass.getpass()
            timestamp = int(datetime.datetime.now().timestamp())
            # login to generate cookies
            payload = {
                'username': username,
                'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:{timestamp}:{password}',
                'queryParams': {},
                'optIntoOneTap': 'false',
                'trustedDeviceRecords': {}
            }
            user = self.session.post(path.LOGIN_URL, data=payload).json()
            try:
                if user["authenticated"]:
                    csrf_token = self.session.cookies.get(
                        "csrftoken", self.session.headers.get('x-csrftoken'))
                    self.session.headers.update({'x-csrftoken': csrf_token})
                    user_id = user["userId"]
                    # test if the account is working
                    user = self.session.get(
                        path.USER_DATA_ENDPOINT.format(user_id)).json()
                    if user['status'] != 'ok':
                        raise Exception(
                            f"Not Working! Check if the given account is working.")
                    user_fullname = user['user']['full_name']
                    print(f"{user_fullname} : Successfully Logged In....")
                    if save_session:
                        session_util.save_session(
                            session=self.session, filename=username)
                    return
                raise Exception("Couldn't Authenticate the user, Try again...",)
            except Exception as error:
                print(f"\n{error}")
                utils.check_for_errors(user)

    @property
    def logged_in(self):
        """Check if user is logged in.

        Returns:
            bool: Returns True if user is logged in.
        """
        if 'sessionid' in self.session.cookies.keys():
            return True
        return False

    def get_session_id(self, username=None, password=None, new_session=False):
        """Get sessionID of the current session OR a new login session. By default returns current one if logged in.

        Args:
            username (str): Username OR Email.
            password (str): Password
            new_session (bool, optional): Set to True if want to get session ID of new session. Otherwise It will return the already logged In session ID. Defaults to False.

        Returns:
            str: Session ID.
        """
        if new_session:
            self.generate_session()
            self.login(username, password)
        if self.logged_in:
            return self.session.cookies['sessionid']
        raise Exception(
            "You are not logged In. Set new_session=True to generate a new session.")

    def get_user_id(self, username):
        if isinstance(username, int) or isinstance(username,str) and username.isnumeric():
            return username
        return self.get_user_info(username)['data']['user']['id']

    def get_user_info(self, username):
        """Extracts user details.

        Args:
            username (str): Instagram username.

        Returns:
            dict: user info like username,id,bio,follower/following count etc.
        """
        response = make_request(path.USER_PROFILE_ENDPOINT.format(username))
        self.shuffle_session()
        return response

    @login_decorator
    def get_user_data(self, user_id):
        """Extracts user details. With Contact Info Like email, phone and address.

        Args:
            user_id (int): User ID of an Instagram User.

        Returns:
            dict: user info along with contact info.
        """
        # returns almost as same data as get_user_info method Except this one returns contact info (email/phone) as well. |LOGIN REQUIRED|
        user_id = self.get_user_id(user_id)
        response = make_request(path.USER_DATA_ENDPOINT.format(user_id))
        self.shuffle_session()
        return response

    def get_user_basic_details(self, username=None, print_formatted=False):
        """Get a brief overview of an Instagram Profile.

        Args:
            username (str, optional): Instagram Username. Defaults to None.
            print_formatted (bool, optional): Print Data in a Structure way. Defaults to False.

        Returns:
            dict: User Data.
        """
        if username is None:
            raise Exception("Username can't be blank. Set a username.")
        user = {}
        user_info = self.get_user_info(username)['data']['user']
        user['id'] = user_info['id']
        user['username'] = user_info['username']
        user['full_name'] = user_info['full_name']
        user['bio'] = user_info['biography']
        user['is_private'] = user_info['is_private']
        user['is_verified'] = user_info['is_verified']
        user['follower_count'] = user_info['edge_followed_by']['count']
        user['following_count'] = user_info['edge_follow']['count']
        user['media_count'] = user_info['edge_owner_to_timeline_media']['count']
        user['website'] = user_info['external_url']
        if print_formatted:
            for key, value in user.items():
                print(f"{key} : {value}")
        return user

    @login_decorator
    def get_user_friends(self, username, followers_list=False, followings_list=False, end_cursor=None, total=None, pagination=True):
        """Fetch follower or following list of a user.

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
        if (not followers_list and not followings_list) or (followers_list and followings_list):
            raise Exception(
                "Set either the followers_list or the followings_list to True.")
        user = self.get_user_basic_details(username)
        data_count = user['follower_count'] if followers_list else user['following_count'] if followings_list else None

        if user['is_private']:
            raise Exception("Account is Private.")

        request_config = {}
        if followers_list and user['is_verified']:
            url = path.GRAPHQL_URL
            max_data = 50
            data_path = ('data', 'user', 'edge_followed_by')
            request_config = request_config | {"query": path.FOLLOWERS_LIST_QUERY, "count": max_data, "user_id": user['id'],
                               "end_cursor": end_cursor, "search_surface":"follow_list_page", "is_graphql":True}
        else:
            if followers_list:
                url = path.USER_FOLLOWERS_ENDPOINT.format(user['id'])
                max_data = 100
            elif followings_list:
                url = path.USER_FOLLOWINGS_ENDPOINT.format(user['id'])
                max_data = 200
            data_path = ("users",)
            request_config = request_config | {"count": max_data, "end_cursor": end_cursor}
        request_config = request_config | {"url": url}
        return self._handle_pagination(data_path=data_path, total=total, request_config=request_config, data_count=data_count, pagination=pagination)

    def get_profile_media(self, username, end_cursor=None, from_date=None, to_date=None, total=None, pagination=True):
        """Returns all media/posts of the given Instagram Profile.

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

        user_id = self.get_user_id(username)
        if from_date is not None:
            from_date = utils.parse_datetime(from_date) + datetime.timedelta(days=1)
        if to_date is not None:
            to_date = utils.parse_datetime(to_date) + datetime.timedelta(days=1)
        request_config = {"query": path.USER_FEED_QUERY, "user_id": user_id, "count": 50, "end_cursor": end_cursor, "is_graphql": True}
        data_path = ('data', 'user', 'edge_owner_to_timeline_media')
        return self._handle_pagination(data_path=data_path, total=total, from_date=from_date, to_date=to_date, request_config=request_config, pagination=pagination)

    def get_post_details(self, post_url):
        """Get details of a particular Instagram Post/Media.

        Args:
            post_url (str): Instagram Post/Picture/Reel URL.

        Returns:
            dict: All the details like post_id,datetime,caption,url,location etc.
        """
        post_id = utils.get_post_id(post_url)
        request_payload = self._generate_request_data(
            query=path.POST_DETAILS_QUERY, shortcode=post_id, is_graphql=True)
        response = make_request(**request_payload)
        self.shuffle_session()
        return response

    def get_media_url(self, response):
        """Extracts High Resolution/Quality Media URL from post details response returned from get_post_details method.

        Args:
            response (dict): Response returned from get_post_details method.

        Returns:
            list/str: Returns List if carousel Else string its a video or a single picture.
        """
        if response['data']['shortcode_media'] is not None:
            media_type = response["data"]["shortcode_media"]["__typename"]
            if media_type == "GraphImage":
                return response['data']['shortcode_media']['display_resources'][-1]['src']
            if media_type == "GraphVideo":
                return response['data']['shortcode_media']['video_url']
            if media_type == "GraphSidecar":
                return [each_carousel['node']['display_resources'][-1]['src'] for each_carousel in response['data']['shortcode_media']['edge_sidecar_to_children']["edges"]]
        return None

    @login_decorator
    def get_about_user(self, username, print_formatted=True):
        """Returns user about details like account location, if running any ads, verified, Joining Date, Verification Date.

        Args:
            username (str): Username of the person
            print_formatted (bool, optional): Returns only necessary and structure data if set to True Else would return the whole dataset. Defaults to True.

        Returns:
            dict: User About Dataset.
        """
        user_id = self.get_user_id(username)
        data = {'referer_type': 'ProfileUsername', 'target_user_id': user_id, 'bk_client_context': {
            'bloks_version': path.ABOUT_USER_QUERY, 'style_id': 'instagram'}, 'bloks_versioning_id': path.ABOUT_USER_QUERY}
        response = make_request(path.ABOUT_USER_URL, method='POST', data=data)
        if print_formatted:
            return utils.format_about_data(response)
        self.shuffle_session()
        return response

    @login_decorator
    def get_hashtag_posts(self, hashtag=None, end_cursor=None, total=None, pagination=True):
        """Get media posts from hashtags.

        Args:
            # hashtag. Defaults to None.
            hashtag (str): Hashtag that you want to extract data from. Accepts both formats i.e. hashtag or
            end_cursor (str, optional): Last endcursor point. (To start from where you left off last time). Defaults to None.
            total (int, optional): Total number of results to extract. Defaults to None. -- Gets all by default.
            pagination (bool, optional): Set to False if want to handle each page request manually. Use end_cursor from the previous page/request to navigate to the next page. Defaults to True.

        Returns:
            dict: Returns data, end_cursor, has_next_page
        """
        if hashtag is None:
            raise Exception("No hashtag was given.")
        hashtag = hashtag.lstrip("#")
        request_config = {"query": path.HASHTAG_QUERY, "hashtag": hashtag, "count": 50, "end_cursor": end_cursor, "is_graphql": True}
        data_path = ('data', 'hashtag', 'edge_hashtag_to_media')
        return self._handle_pagination(data_path=data_path, total=total, request_config=request_config, pagination=pagination)



if __name__ == "__main__":
    pass
