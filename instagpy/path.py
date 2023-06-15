from urllib.parse import urljoin

# URL Path & Endpoints
BASE_URL = "https://www.instagram.com/"
LOGIN_URL = "https://www.instagram.com/accounts/login/ajax/"
LOGIN_PAGE_URL = "https://www.instagram.com/accounts/login/"
LOCATION_URL = "https://www.instagram.com/explore/locations/{}"
LOCATION_ENDPOINT = "https://www.instagram.com/api/v1/locations/web_info/"
# USER_DATA_ENDPOINT = "https://i.instagram.com/api/v1/users/{}/full_detail_info/"
# USER_DATA_ENDPOINT = "https://i.instagram.com/api/v1/users/web_profile_info/?username={}"
USER_DATA_ENDPOINT = "https://i.instagram.com/api/v1/users/{}/info"
USER_PROFILE_ENDPOINT = "https://www.instagram.com/api/v1/users/web_profile_info/?username={}"
META_DATA_URL = "https://www.instagram.com/data/shared_data/?__a=1"

# user_followers_endpoint returns max 100 results in a single request
# Doesnt work with verified accounts
USER_FOLLOWERS_ENDPOINT = "https://i.instagram.com/api/v1/friendships/{}/followers/"
# USER_FOLLOWINGS_ENDPOINT returns max 200 results in a single request
USER_FOLLOWINGS_ENDPOINT = "https://i.instagram.com/api/v1/friendships/{}/following/"

STORY_ENDPOINT = "https://i.instagram.com/api/v1/feed/reels_media/?reel_ids={}"
# STORY_ENDPOINT = "https://i.instagram.com/api/v1/feed/reels_media/?media_id={}"
LOCATION_ENDPOINT = "https://www.instagram.com/api/v1/locations/web_info/"


# graphql query and path
GRAPHQL_URL = urljoin(BASE_URL, "/graphql/query/")
# return 50 at a time
POST_DETAILS_QUERY = "9f8827793ef34641b2fb195d4d41151c"
USER_FEED_QUERY = "69cba40317214236af40e7efa697781d"
# followers_list_query & following_list_query - both return max 50 results in a single request but work with blue tick verified accounts.
FOLLOWERS_LIST_QUERY = "7dd9a7e2160524fd85f50317462cff9f"
FOLLOWING_LIST_QUERY = "c56ee0ae1f89cdbd1c89e2bc6b8f3d18"

ABOUT_USER_URL = "https://i.instagram.com/api/v1/bloks/apps/com.instagram.interactions.about_this_account/"
ABOUT_USER_QUERY = "8ca96ca267e30c02cf90888d91eeff09627f0e3fd2bd9df472278c9a6c022cbb"

HASHTAG_QUERY = "9b498c08113f1e09617a1703c22b2f32"

if __name__ == '__main__':
    pass
