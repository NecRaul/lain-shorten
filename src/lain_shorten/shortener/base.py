import time

import requests

from ..util import ensure_url_has_scheme, is_valid_url
from ..version import __version__


class BaseShortener:
    name = ""
    endpoint = ""
    method = "POST"
    url_format = False
    request_delay = 0.0
    last_request_time = 0.0

    @classmethod
    def shorten(cls, url):

        url = url.strip()
        url = ensure_url_has_scheme(url)

        if not is_valid_url(url):
            raise ValueError(f"{url} is not a valid supported URL.")

        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": f"lain-shorten/{__version__} (https://github.com/NecRaul/lain-shorten)",
        }

        try:
            cls.wait_if_needed()
            response = requests.request(
                cls.method,
                cls.build_endpoint(url),
                data=cls.build_data(url),
                headers=headers,
                timeout=10,
            )
            response.raise_for_status()
        finally:
            cls.last_request_time = time.monotonic()

        result = response.text.strip()

        if not result:
            raise ValueError("Server returned an empty response.")

        return result

    @classmethod
    def build_endpoint(cls, url):
        if cls.url_format:
            return cls.endpoint.format(url=requests.utils.quote(url, safe=""))
        return cls.endpoint

    @classmethod
    def build_data(cls, url):
        if cls.url_format:
            return None
        return {"url": url}

    @classmethod
    def wait_if_needed(cls):
        if cls.request_delay <= 0:
            return

        elapsed = time.monotonic() - cls.last_request_time
        remaining = cls.request_delay - elapsed

        if remaining > 0:
            time.sleep(remaining)
