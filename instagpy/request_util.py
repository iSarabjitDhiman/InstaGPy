import requests
import bs4
from . import utils
from . import config


def make_request(url, session=None, method=None, max_retries=None, timeout=None, **kwargs):
    if session is None:
        raise NameError("name 'session' is not defined.")
    if not isinstance(session, requests.Session):
        raise TypeError(f"Invalid session type. {session} is not a requests.Session Object...")
    if method is None:
        method = "GET"
    if max_retries is None:
        max_retries = config.MAX_RETRIES or 3
    if timeout is None:
        timeout = config.TIMEOUT or 30
    for retry_count, _ in enumerate(range(max_retries), start=1):
        try:
            response_text = ""
            response = session.request(method, url, timeout=timeout, **kwargs)
            soup = bs4.BeautifulSoup(response.content, "lxml")
            if "json" in response.headers["Content-Type"]:
                return utils.check_for_errors(response.json())
            response_text = "\n".join(
                [line.strip() for line in soup.text.split("\n") if line.strip()])
            response.raise_for_status()
            return soup
        except KeyboardInterrupt:
            print("Keyboard Interruption...")
            return
        except requests.exceptions.RequestException as error:
            print(f"\nRetry No. ==> {retry_count} : {error}\n{response_text}")
        except Exception as error:
            print(f"\nRetry No. ==> {retry_count} : {error}\n{response_text}")


if __name__ == '__main__':
    pass
