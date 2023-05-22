from urllib.parse import urljoin

# URL Path & Endpoints
base_url = "https://www.instagram.com/"
login_url = "https://www.instagram.com/accounts/login/ajax/"
login_page_url = "https://www.instagram.com/accounts/login/"
location_url = "https://www.instagram.com/explore/locations/{}"
location_endpoint = "https://www.instagram.com/api/v1/locations/web_info/"
# user_data_endpoint = "https://i.instagram.com/api/v1/users/{}/full_detail_info/"
# user_data_endpoint = "https://i.instagram.com/api/v1/users/web_profile_info/?username={}"
user_data_endpoint = "https://i.instagram.com/api/v1/users/{}/info"
user_profile_endpoint = "https://i.instagram.com/api/v1/users/web_profile_info/?username={}"


# user_followers_endpoint returns max 100 results in a single request
# Doesnt work with verified accounts
user_followers_endpoint = "https://i.instagram.com/api/v1/friendships/{}/followers/"
# user_followings_endpoint returns max 200 results in a single request
user_followings_endpoint = "https://i.instagram.com/api/v1/friendships/{}/following/"

story_endpoint = "https://i.instagram.com/api/v1/feed/reels_media/?reel_ids={}"
# story_endpoint = "https://i.instagram.com/api/v1/feed/reels_media/?media_id={}"
location_endpoint = "https://www.instagram.com/api/v1/locations/web_info/"


# graphql query and path
graphql_url = urljoin(base_url, "/graphql/query/")
# return 50 at a time
post_details_query = "9f8827793ef34641b2fb195d4d41151c"
user_feed_query = "69cba40317214236af40e7efa697781d"
# followers_list_query & following_list_query - both return max 50 results in a single request but work with blue tick verified accounts.
followers_list_query = "7dd9a7e2160524fd85f50317462cff9f"
following_list_query = "c56ee0ae1f89cdbd1c89e2bc6b8f3d18"

about_user_url = "https://i.instagram.com/api/v1/bloks/apps/com.instagram.interactions.about_this_account/"
about_user_query = "8ca96ca267e30c02cf90888d91eeff09627f0e3fd2bd9df472278c9a6c022cbb"


if __name__ == '__main__':
    pass
