from urllib.parse import parse_qs, urlparse


def ensure_url_has_scheme(url):
    if urlparse(url).scheme:
        return url

    if not url.startswith(("//",)):
        return f"http://{url}"
    return url


def _validate_network(result):
    return bool(result.netloc)


def _validate_handle(result):
    return bool(result.path and "@" in result.path)


def _validate_phone(result):
    return bool(result.path)


def _validate_magnet(result):
    query = parse_qs(result.query)
    return bool(query.get("xt"))


VALIDATORS = {
    "http": _validate_network,
    "https": _validate_network,
    "irc": _validate_network,
    "ircs": _validate_network,
    "ssh": _validate_network,
    "mailto": _validate_handle,
    "xmpp": _validate_handle,
    "sms": _validate_phone,
    "tel": _validate_phone,
    "magnet": _validate_magnet,
}


def is_valid_url(url):
    try:
        result = urlparse(url)
        validator = VALIDATORS.get(result.scheme)
        return validator(result) if validator else False
    except ValueError:
        return False
