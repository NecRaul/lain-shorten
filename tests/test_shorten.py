import time
import unittest
from urllib.parse import urlparse

import requests

from lain_shorten import __version__
from lain_shorten.shortener import LainLaShortener

allowed_shorteners = {
    LainLaShortener: ("lain.la",),
}


class ShortenIntegrationTests(unittest.TestCase):
    def _assert_short_url(self, url, expected_domains, verify_redirect=True):
        self.assertTrue(url)
        self.assertTrue(url.startswith("http"))

        hostname = urlparse(url).hostname
        self.assertTrue(hostname)
        self.assertTrue(
            any(
                hostname == domain.lower().rstrip("/")
                or hostname.endswith("." + domain.lower().rstrip("/"))
                for domain in expected_domains
            ),
            f"Unexpected URL format for {url}",
        )

        if not verify_redirect:
            return

        last_error = None
        for _ in range(5):
            try:
                r = requests.get(
                    url,
                    timeout=10,
                    headers={
                        "User-Agent": f"lain-shorten-tests/{__version__} (https://github.com/NecRaul/lain-shorten)"
                    },
                    allow_redirects=False,
                )
                self.assertIn(r.status_code, (301, 302, 303, 307, 308))
                return
            except requests.RequestException as error:
                last_error = error
                time.sleep(1)

        self.fail(f"Short URL not reachable: {last_error}")

    def _shorten(self, url):
        for shortener_class, expected_domains in allowed_shorteners.items():
            yield (
                shortener_class,
                shortener_class().shorten(url),
                expected_domains,
            )

    def test_shorten_http_url(self):
        for shortener_class, url, domains in self._shorten("https://example.com"):
            with self.subTest(shortener=shortener_class.__name__):
                self._assert_short_url(url, domains)

    def test_shorten_https_url(self):
        for shortener_class, url, domains in self._shorten("https://kuroneko.dev"):
            with self.subTest(shortener=shortener_class.__name__):
                self._assert_short_url(url, domains)

    def test_shorten_irc_url(self):
        for shortener_class, url, domains in self._shorten(
            "irc://irc.example.com/#test"
        ):
            with self.subTest(shortener=shortener_class.__name__):
                self._assert_short_url(url, domains)

    def test_shorten_ircs_url(self):
        for shortener_class, url, domains in self._shorten(
            "ircs://irc.example.com/#test"
        ):
            with self.subTest(shortener=shortener_class.__name__):
                self._assert_short_url(url, domains)

    def test_shorten_ssh_url(self):
        for shortener_class, url, domains in self._shorten("ssh://user@example.com"):
            with self.subTest(shortener=shortener_class.__name__):
                self._assert_short_url(url, domains)

    def test_shorten_mailto(self):
        for shortener_class, url, domains in self._shorten("mailto:test@example.com"):
            with self.subTest(shortener=shortener_class.__name__):
                self._assert_short_url(url, domains)

    def test_shorten_xmpp(self):
        for shortener_class, url, domains in self._shorten("xmpp:test@example.com"):
            with self.subTest(shortener=shortener_class.__name__):
                self._assert_short_url(url, domains)

    def test_shorten_sms(self):
        for shortener_class, url, domains in self._shorten("sms:+15551234567"):
            with self.subTest(shortener=shortener_class.__name__):
                self._assert_short_url(url, domains)

    def test_shorten_tel(self):
        for shortener_class, url, domains in self._shorten("tel:+15551234567"):
            with self.subTest(shortener=shortener_class.__name__):
                self._assert_short_url(url, domains)

    def test_shorten_magnet(self):
        magnet = "magnet:?xt=urn:btih:0123456789abcdef0123456789abcdef01234567&dn=test"

        for shortener_class, url, domains in self._shorten(magnet):
            with self.subTest(shortener=shortener_class.__name__):
                self._assert_short_url(url, domains)

    def test_shorten_without_scheme(self):
        for shortener_class, url, domains in self._shorten("example.com"):
            with self.subTest(shortener=shortener_class.__name__):
                self._assert_short_url(url, domains)

    def test_invalid_url_fails(self):
        for shortener_class in allowed_shorteners:
            with self.subTest(shortener=shortener_class.__name__):
                with self.assertRaises(ValueError):
                    shortener_class().shorten("ftp://example.com")


if __name__ == "__main__":
    unittest.main()
