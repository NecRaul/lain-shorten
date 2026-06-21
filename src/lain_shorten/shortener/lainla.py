from .base import BaseShortener


class LainLaShortener(BaseShortener):
    name = "lainla"
    endpoint = "https://s.lain.la"
    method = "POST"
    url_format = False
    request_delay = 0.0
