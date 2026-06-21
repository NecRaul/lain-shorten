from urllib.parse import parse_qs, urlparse

import requests


def ensure_url_has_scheme(url):
    if urlparse(url).scheme:
        return url

    if not url.startswith(("//",)):
        return f"http://{url}"
    return url


def is_valid_url(url):
    try:
        result = urlparse(url)
        validator = VALIDATORS.get(result.scheme)
        return validator(result) if validator else False
    except ValueError:
        return False


def validate_network(result):
    return bool(result.netloc)


def validate_handle(result):
    return bool(result.path and "@" in result.path)


def validate_phone(result):
    return bool(result.path)


def validate_magnet(result):
    query = parse_qs(result.query)
    return bool(query.get("xt"))


VALIDATORS = {
    "http": validate_network,
    "https": validate_network,
    "irc": validate_network,
    "ircs": validate_network,
    "ssh": validate_network,
    "mailto": validate_handle,
    "xmpp": validate_handle,
    "sms": validate_phone,
    "tel": validate_phone,
    "magnet": validate_magnet,
}


def shorten_url(url):
    url = url.strip()
    url = ensure_url_has_scheme(url)

    if not is_valid_url(url):
        raise ValueError(f"'{url}' is not a valid supported URL.")

    response = requests.post(
        "https://s.lain.la",
        data={"url": url},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        timeout=10,
    )
    response.raise_for_status()
    result = response.text.strip()
    if not result:
        raise ValueError("Server returned an empty response.")

    return result
