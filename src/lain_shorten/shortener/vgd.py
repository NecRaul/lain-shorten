from lain_shorten.shortener.base import BaseShortener


class VgdShortener(BaseShortener):
    name = "vgd"
    endpoint = "https://v.gd/create.php?format=simple&url={url}"
    method = "GET"
    url_format = True
    request_delay = 0.0
