import requests
import bs4


def make_request(url, session=None, method=None, max_retries=None, timeout=None, **kwargs):
    if method is None:
        method = "GET"
    if max_retries is None:
        max_retries = 3
    if session is None:
        session = requests.Session()
    if timeout is None:
        timeout = 30
    for retry_count, retry in enumerate(range(max_retries), start=1):
        try:
            response = session.request(method, url, timeout=timeout, **kwargs)
            response.raise_for_status()
            soup = bs4.BeautifulSoup(response.content, "lxml")
            if "json" in response.headers["Content-Type"]:
                return response.json()
            return soup
        except KeyboardInterrupt:
            print("Keyboard Interruption...")
            return
        except requests.exceptions.RequestException as error:
            print(f"Retry No. ==> {retry_count}", error)
        except Exception as error:
            print(f"Retry No. ==> {retry_count}", error)


if __name__ == '__main__':
    pass
