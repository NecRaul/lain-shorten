from lain_shorten.shortener.base import BaseShortener


class OnePointShortener(BaseShortener):
    name = "onepoint"
    endpoint = "https://thakkaha.dev.fast.sheridanc.on.ca/1pt/addURL.php?url={url}"
    method = "GET"
    url_format = True
    request_delay = 0.0

    @classmethod
    def parse_response(cls, response):
        try:
            data = response.json()
        except ValueError:
            raise ValueError(f"API returned invalid JSON: {response.text}")
        short = data.get("short")
        if not short:
            raise ValueError(f"API returned invalid format: {response.text}")
        return f"https://1pt.co/{short}"
