from .base import BaseShortener


class WildLainShortener(BaseShortener):
    name = "wildlain"
    endpoint = "https://s.wildla.in/register/{url}"
    method = "GET"
    url_format = True
    request_delay = 10.0
