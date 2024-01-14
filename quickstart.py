from instagpy import InstaGPy
from instagpy import config


def main():
    #config.TIMEOUT = 5
    #config.PROXY = {'http': 'proxy_here', 'https': 'proxy_here'}
    insta = InstaGPy(use_mutiple_account=False, session_ids=None,
                     min_requests=None, max_requests=None)
    insta.get_user_basic_details('champagnepapi', print_formatted=True)
    #insta.login(username=None, password=None, show_saved_sessions=False, save_session=True)
    # insta.logged_in
    # user_id = insta.get_user_id(username=None)
    # user = insta.get_user_basic_details(username=None)
    # user_info = insta.get_user_info(username=None)
    # user_data = insta.get_user_data(user_id=None)
    # user_friends = insta.get_user_friends(username=None, followers_list=False, followings_list=False,
    #                                       end_cursor=None, max=None, save_to_database=False)
    # user_profile_media = insta.get_profile_media(username=None, end_cursor=None,
    #                                              from_date=None, to_date=None, max=None)
    # post_details = insta.get_post_details(post_url=None)
    # download_url = insta.get_media_url(response=None)


if __name__ == "__main__":
    main()
