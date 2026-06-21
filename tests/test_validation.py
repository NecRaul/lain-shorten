import unittest

from lain_shorten.util import ensure_url_has_scheme, is_valid_url


class UrlValidationTests(unittest.TestCase):
    def test_protocol_less_domain_is_normalized(self):
        self.assertEqual(
            ensure_url_has_scheme("example.com"),
            "http://example.com",
        )

    def test_supported_network_urls(self):
        supported_urls = [
            "https://example.com",
            "ssh://abc@example.com",
            "irc://irc.example.com/channel",
            "ircs://irc.example.com/channel",
        ]

        for url in supported_urls:
            with self.subTest(url=url):
                self.assertTrue(is_valid_url(url))

    def test_supported_handle_urls(self):
        supported_urls = [
            "mailto:abc@example.com",
            "xmpp:abc@example.com",
        ]

        for url in supported_urls:
            with self.subTest(url=url):
                self.assertTrue(is_valid_url(url))

    def test_supported_phone_urls(self):
        supported_urls = [
            "tel:+15551234567",
            "sms:+15551234567",
        ]

        for url in supported_urls:
            with self.subTest(url=url):
                self.assertTrue(is_valid_url(url))

    def test_magnet_is_supported(self):
        self.assertTrue(
            is_valid_url(
                "magnet:?xt=urn:btih:0123456789abcdef0123456789abcdef01234567&dn=Example"
            )
        )

    def test_invalid_cases(self):
        invalid_urls = [
            "magnet:?dn=Example",
            "mailto:not-an-email",
            "xmpp:invalid",
            "tel:",
            "ftp://ftp.example.com/files",
            "ftps://secure.example.com/files",
            "sftp://user@example.com/home/user",
            "git://git.example.com/my/repo.git",
            "ws://example.com/socket",
            "wss://example.com/socket",
            "file:///home/user/Documents/example.txt",
            "customscheme://example.com",
        ]

        for url in invalid_urls:
            with self.subTest(url=url):
                self.assertFalse(is_valid_url(url))


if __name__ == "__main__":
    unittest.main()
