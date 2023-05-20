import datetime
from urllib.parse import urlparse


def format_datetime(timestamp):
    return datetime.datetime.fromtimestamp(timestamp).strftime("%I:%M:%p")


def parse_datetime(datetime_string):
    return datetime.datetime.strptime(datetime_string, "%Y-%m-%d")


def get_post_id(post_url, is_story=False):
    if is_story or "stories" in post_url:
        post_data = urlparse(post_url).path.split('/stories/')[-1].split('/')
    else:
        post_data = urlparse(post_url).path.split('/p/')[-1].split('/')
    post_data = [data for data in post_data if data.strip()]
    post_id = post_data[1] if len(post_data) > 1 else post_data[0]

    return post_id


if __name__ == '__main__':
    pass
