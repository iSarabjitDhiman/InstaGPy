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


def format_about_data(response, placeholder=None):
    if placeholder is None or not isinstance(placeholder, dict):
        placeholder = {}
    if isinstance(response, list):
        for item in response:
            format_about_data(item, placeholder)
    elif isinstance(response, dict):
        if 'children' in response.keys():
            if isinstance(response['children'], list):
                if any('bk.components.Text' in item for item in response['children']):
                    try:
                        placeholder[response['children'][0]['bk.components.Text']['text']
                                    ] = response['children'][1]['bk.components.RichText']['children'][0]['bk.components.TextSpan']['text']
                    except:
                        try:
                            placeholder[response['children'][0]
                                        ['bk.components.Text']['text']] = None
                        except:
                            pass
        if 'data' in response.keys():
            if isinstance(response['data'], list):
                placeholder.update({item['data']['key']: item['data']['initial_lispy'] for item in filter(
                    lambda item: ('key' in item['data'] and 'initial_lispy' in item['data']), response['data'])})
        for value in response.values():
            format_about_data(value, placeholder)
    else:
        pass

    for key, value in placeholder.items():
        if value is None:
            continue
        if 'bk.action.array.Make' in value and key.endswith('about_this_account_country'):
            placeholder[key] = value.split(
                'bk.action.array.Make,')[-1].split(")")[0].replace('"', '').strip()
    return placeholder


def check_for_errors(response):
    if isinstance(response, dict):
        if "status" in response.keys():
            if response["status"] == "ok":
                return response
            if response["status"] != "ok":
                if "message" in response.keys():
                    print(response)
                    raise Exception(response['message'])
    return response


if __name__ == '__main__':
    pass
