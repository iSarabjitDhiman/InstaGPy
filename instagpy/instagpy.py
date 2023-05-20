import requests
import json
import datetime
import time
import getpass
import random
from .path import *
from .request_util import make_request
from . import session_util
from . import utils

user_agent = "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_3 like Mac OS X) AppleWebKit/603.3.8 (KHTML, like Gecko) Mobile/14G60 Instagram 12.0.0.16.90 (iPhone9,4; iOS 10_3_3; en_US; en-US; scale=2.61; gamut=wide; 1080x1920"


class InstaGPy:

    def __init__(self, max_retries=None, proxies=None, use_mutiple_account=False, session_ids=None, min_requests=None, max_requests=None):
        """

        Args:
            max_retries (int, optional): Number of retires for each request. Defaults to None.
            proxies (dict, optional): Proxies as a dictionary {'http': proxy_here,'https':proxy_here}. Residential Proxies are recommended. Defaults to None.
            use_mutiple_account (bool, optional): Set to True if want to scrape data with mutiple account sessions So that you don't get blocked. Defaults to False.
            session_ids (list, optional): List of Session IDs from Cookies. Applicable only if use_mutiple_accounts is True. Defaults to False.
            min_requests (int, optional): Minimum requests to make before shuffling a session ID. Defaults to None.
            max_requests (int, optional): Maximum requests to make before shuffling a session ID. Defaults to None.
        """
        if use_mutiple_account and not session_ids:
            raise Exception(
                'Either Pass a list of session_ids or set use_multiple_account to False.')
        if use_mutiple_account and session_ids:
            self.session_ids = session_ids
            self.current_request_number = 1
            # shuffle session randomly after every nth request.
            self.min_requests = min_requests or 3
            self.max_requests = max_requests or 6
            self.shuffle_session_after = random.randint(
                self.min_requests, self.max_requests)
            self.session_ids_container = None
        self.use_mutiple_account = use_mutiple_account
        self.max_retries = max_retries or 3
        self.session = requests.Session()
        if proxies is not None:
            self.session.proxies = proxies
            self.session.verify = False
        self.generate_session()

    def generate_session(self, session_id=None):
        """Generates Required Headers and Cookies. OR Generates Session from an existing Session ID.

        Args:
            session_id (str, optional): Session Id from Instagram Session Cookies. Defaults to None.
        """
        self.session.headers.update(
            {"User-Agent": user_agent})
        make_request(base_url, session=self.session,
                     max_retries=self.max_retries)
        response = requests.get(login_url)
        if not response.cookies:
            for _ in range(self.max_retries):
                response = self.session.get(login_url)
                if response.cookies:
                    break
        csrf_token = dict(response.cookies)["csrftoken"]
        if session_id:
            "load an existing session with session_id"
            self.session.cookies.update({'sessionid': session_id})
            return
        self.session.cookies = response.cookies
        self.session.headers.update(
            {'x-csrftoken': csrf_token, 'X-Requested-With': "XMLHttpRequest", 'Referer': login_page_url})

    def shuffle_session(self):
        if self.current_request_number % self.shuffle_session_after == 0:
            self.shuffle_session_after = random.randint(
                self.min_requests, self.max_requests)
            if not self.session_ids_container:
                self.session_ids_container = self.session_ids.copy()
            session_id = self.session_ids_container.pop()
            self.generate_session(session_id=session_id)

    def generate_query(self, query=None, count=None, user_id=None, end_cursor=None, search_surface=None, shortcode=None, is_graphql=False):
        """Generates query paramters for instagram api requests.

        Args:
            query (str, optional): Query endpoint. Defaults to None.
            count (int, optional): Number of results per request to extract from Instagram Database. Defaults to None.
            user_id (int, optional): User Profile ID. Defaults to None.
            end_cursor (str, optional): Last endcursor point. (To start from where you left off last time). Defaults to None.
            search_surface (str, optional): Source of request. Defaults to None.
            shortcode (str, optional): Instagram Post ID. Defaults to None.
            is_graphql (bool, optional): If its a Graphql query or standard request. Defaults to False.

        Returns:
            dict: query paramters
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

            params["variables"] = json.dumps(data)
        else:
            if count:
                params["count"] = count
            if search_surface is not None:
                params["search_surface"] = search_surface
            if end_cursor is not None:
                params["max_id"] = end_cursor

        return params

    def login(self, username=None, password=None, show_saved_sessions=True, save_session=True):
        """Login Into a user account for Data Scraping Purpose.

        Args:
            username (str, optional): Instgram Username or Email. Defaults to None.
            password (str, optional): Password. Defaults to None.
            show_saved_sessions (bool, optional): Shows saved sessions before logging into new account. Defaults to True.
            save_session (bool, optional): Save session if want to use it without logging in manually each time. Defaults to True.

        Returns:
            dict: Response from server whether got logged in.
        """
        self.generate_session()
        if show_saved_sessions:
            session_util.load_session(session=self.session)
            return
        if username is None:
            username = str(input("Enter Your Username or Email : ")).strip()
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
        response = self.session.post(login_url, data=payload).json()
        try:
            if response["authenticated"]:
                print("\nSuccessfully Logged In....")
                if save_session:
                    session_util.save_session(
                        session=self.session, filename=username)
                return
            raise Exception("Couldn't LogIn, Try again...")
        except Exception as e:
            print('\n', e)
            return response

    def logged_in(self):
        """Check if user is logged in.

        Returns:
            bool: Returns True if user is logged in.
        """
        if 'sessionid' in self.session.cookies.keys():
            return True
        return False

    def get_user_id(self, username):
        if isinstance(username, int) or username.isnumeric():
            return username
        return self.get_user_info(username)['data']['user']['id']

    def get_user_info(self, username):
        """Extracts user details.

        Args:
            username (str): Instagram username.

        Returns:
            dict: user info like username,id,bio,follower/following count etc.
        """
        return make_request(user_profile_endpoint.format(username), session=self.session, max_retries=self.max_retries)

    def get_user_data(self, user_id):
        """Extracts user details. With Contact Info Like email, phone and address.

        Args:
            user_id (int): User ID of an Instagram User.

        Returns:
            dict: user info along with contact info.
        """
        # returns almost as same data as get_user_info method Except this one returns contact info (email/phone) as well. |LOGIN REQUIRED|
        if not self.logged_in():
            self.login()
        user_id = self.get_user_id(user_id)
        response = make_request(user_data_endpoint.format(
            user_id), session=self.session, max_retries=self.max_retries)
        if self.use_mutiple_account:
            self.current_request_number += 1
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

    def get_user_friends(self, username, followers_list=False, followings_list=False, end_cursor=None, max=None):
        """Fetch follower or following list of a user.

        Args:
            username (str): Instagram Username.
            followers_list (bool, optional): Set True if want to extract user's followers list. Defaults to False.
            followings_list (bool, optional): Set True if want to extract user's followings list. Defaults to False.
            end_cursor (str, optional): Last endcursor point. (To start from where you left off last time). Defaults to None.
            max (int, optional): Number of results per request to extract from Instagram Database. Defaults to None.

        Returns:
            list: All followers or followings.
        """
        if (not followers_list and not followings_list) or (followers_list and followings_list):
            raise Exception(
                "Set either the followers_list or the followings_list to True.")
        if not self.logged_in():
            self.login()
        user = self.get_user_basic_details(username)
        count = user['follower_count'] if followers_list else user['following_count'] if followings_list else None

        if user['is_private']:
            raise Exception("Account is Private.")

        user_friends = []
        print(f'Started at : {utils.format_datetime(time.time())}\n')
        while True:
            if followers_list and user['is_verified']:
                url = graphql_url
                max_data = 50
                query_params = self.generate_query(query=followers_list_query, count=max_data, user_id=user['id'],
                                                   end_cursor=end_cursor, search_surface="follow_list_page", is_graphql=True)
            else:
                if followers_list:
                    url = user_followers_endpoint.format(user['id'])
                    max_data = 100
                elif followings_list:
                    url = user_followings_endpoint.format(user['id'])
                    max_data = 200
                query_params = self.generate_query(
                    count=max_data, end_cursor=end_cursor)

            try:
                response = make_request(
                    url, params=query_params, session=self.session, max_retries=self.max_retries)
                if followers_list and user['is_verified']:
                    data = response['data']['user']['edge_followed_by']
                    has_next_page = data['page_info']['has_next_page']
                    end_cursor = data['page_info']['end_cursor']
                    data = data['edges']
                else:
                    data = response['users']
                    if 'next_max_id' in response.keys():
                        end_cursor = response['next_max_id']
                    has_next_page = response['big_list']
                user_friends.extend(data)

                print(
                    f"{user['username']} : {len(user_friends)} / {count}", end="\r")
                if not has_next_page or (max is not None and len(user_friends) >= max):
                    return user_friends

                if self.use_mutiple_account:
                    self.current_request_number += 1
                    self.shuffle_session()

            except ConnectionError as error:
                print(error)
                continue

            except Exception as error:
                print(error)
                return user_friends

    def get_profile_media(self, username, end_cursor=None, from_date=None, to_date=None, max=None):
        """Returns all media/posts of the given Instagram Profile.

        Args:
            username (str): Instagram Username.
            end_cursor (str, optional): Last endcursor point. (To start from where you left off last time). Defaults to None.
            from_date (str, optional): FORMAT - 'Year-Month-Date' Fetch posts starting from a specified period of time. Defaults to None.
            to_date (str, optional): FORMAT - 'Year-Month-Date'  Fetch posts upto a specified period of time. Defaults to None.
            max (int, optional): Number of results per request to extract from Instagram Database. Defaults to None.

        Returns:
            list: All Posts of the given Instagram user.
        """
        def filter_by_date(user_posts):
            posts_data = []
            for each_post in user_posts:
                post_date = datetime.datetime.fromtimestamp(
                    each_post['node']['taken_at_timestamp'])
                if from_date is not None:
                    if post_date <= from_date:
                        continue
                if to_date is not None:
                    if post_date >= to_date:
                        continue
                posts_data.append(each_post)
                if max is not None and (len(user_posts_data) + len(posts_data)) >= max:
                    return posts_data
            return posts_data

        user = self.get_user_basic_details(username)
        user_id = user['id']
        user_posts_data = []
        if from_date is not None:
            from_date = utils.parse_datetime(from_date)
            from_date = from_date + datetime.timedelta(days=1)
        if to_date is not None:
            to_date = utils.parse_datetime(to_date)
            to_date = to_date + datetime.timedelta(days=1)
        print(f'Started at : {utils.format_datetime(time.time())}\n')
        try:
            while True:
                query_params = self.generate_query(
                    query=user_feed_query, user_id=user_id, count=50, end_cursor=end_cursor, is_graphql=True)
                try:
                    response = make_request(
                        graphql_url, params=query_params, session=self.session, max_retries=self.max_retries)
                    data = response['data']['user']['edge_owner_to_timeline_media']
                    posts_count = data['count']
                    has_next_page = data['page_info']['has_next_page']
                    cursor = data['page_info']['end_cursor']
                    if cursor:
                        end_cursor = cursor
                    user_posts_data.extend(filter_by_date(data['edges']))
                    print(
                        f"{username} : {len(user_posts_data)} of {posts_count}", end="\r")

                except ConnectionError as error:
                    print(error)
                    continue

                except Exception as error:
                    print(error)
                    return user_posts_data

                if from_date:
                    if any(datetime.datetime.fromtimestamp(post['node']['taken_at_timestamp']) <= from_date for post in data['edges']):
                        return user_posts_data

                if not has_next_page or (max is not None and len(user_posts_data) >= max):
                    return user_posts_data

                if self.use_mutiple_account:
                    self.current_request_number += 1
                    self.shuffle_session()

        except Exception as e:
            print(e)

    def get_post_details(self, post_url):
        """Get details of a particular Instagram Post/Media.

        Args:
            post_url (str): Instagram Post/Picture/Reel URL.

        Returns:
            dict: All the details like post_id,datetime,caption,url,location etc.
        """
        post_id = utils.get_post_id(post_url)
        url = graphql_url
        query_params = self.generate_query(
            query=post_details_query, shortcode=post_id, is_graphql=True)
        return make_request(url, params=query_params, session=self.session, max_retries=self.max_retries)

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


if __name__ == "__main__":
    pass
