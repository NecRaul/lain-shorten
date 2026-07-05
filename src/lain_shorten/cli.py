import argparse
import json
import sys
import webbrowser

import requests

from lain_shorten import __version__, config, shortener, util


def main():
    allowed_shorteners = {
        "lainla": "LainLa",
        "wildlain": "WildLain",
        "vgd": "Vgd",
    }
    parser = argparse.ArgumentParser(
        description="Shorten URLs using various URL shorteners",
        formatter_class=argparse.HelpFormatter,
        epilog="Example: %(prog)s --shortener lainla https://kuroneko.dev/ https://github.com/NecRaul",
    )
    parser.add_argument("-v", "--version", action="version", version=__version__)
    config_group = parser.add_mutually_exclusive_group()
    config_group.add_argument("--config", help="load configuration from file")
    config_group.add_argument(
        "--no-config", action="store_true", help="ignore configuration file"
    )
    config_group.add_argument(
        "--init-config",
        nargs="?",
        const=None,
        default=argparse.SUPPRESS,
        help="create default configuration file",
    )
    parser.add_argument(
        "--show-config",
        action="store_true",
        help="show effective configuration and exit",
    )
    parser.add_argument(
        "--shortener",
        nargs="?",
        default=argparse.SUPPRESS,
        choices=[*allowed_shorteners.keys(), "all"],
        help="shortener to use",
    )
    parser.add_argument(
        "-o",
        "--open",
        action="store_true",
        default=argparse.SUPPRESS,
        help="open each generated short URL in your default browser",
    )
    parser.add_argument("urls", nargs="*", default=[], help="URL(s) to be shortened")

    args = parser.parse_args()

    if hasattr(args, "init_config"):
        path = config.save_config(config.DEFAULT_CONFIG, args.init_config)
        print(f"Config created at {path}", file=sys.stderr)
        if args.show_config:
            print(json.dumps(config.DEFAULT_CONFIG, indent=2))
        return

    cfg = config.load_effective_config(path=args.config, no_config=args.no_config)

    if args.show_config:
        print(json.dumps(cfg, indent=2))
        return

    shortener_service = getattr(args, "shortener", None) or cfg.get(
        "default_shortener", "lainla"
    )

    if shortener_service not in allowed_shorteners and shortener_service != "all":
        parser.error(f"Invalid shortener in config: {shortener_service}")

    if not args.urls:
        parser.error("no URL(s) specified")

    selected_shorteners = (
        list(allowed_shorteners.keys())
        if shortener_service == "all"
        else [shortener_service]
    )

    shortened_urls = []
    has_error = False

    for shortener_name in selected_shorteners:
        shortener_class_name = f"{allowed_shorteners[shortener_name]}Shortener"
        if not hasattr(shortener, shortener_class_name):
            continue
        shortener_class = getattr(shortener, shortener_class_name)

        for url_full in args.urls:
            try:
                shortener_instance = shortener_class()
                url_short = shortener_instance.shorten(url_full)
                if util.is_valid_url(url_short):
                    print(f"{url_full}: {url_short}")
                    shortened_urls.append(url_short)
                else:
                    print(
                        f"Error: API returned invalid format for "
                        f"{url_full}: {url_short}",
                        file=sys.stderr,
                    )
                    has_error = True
            except ValueError as e:
                print(f"Value Error: {e}", file=sys.stderr)
                has_error = True
                continue
            except requests.RequestException as e:
                print(f"Network error: {e}", file=sys.stderr)
                has_error = True
                continue

    if shortened_urls:
        all_urls = "\n".join(shortened_urls)
        try:
            import pyperclip

            pyperclip.copy(all_urls)
            print("\nURL(s) copied to clipboard", file=sys.stderr)
        except Exception:
            pass

        if hasattr(args, "open") or cfg.get("open_urls", False):
            for url_short in shortened_urls:
                webbrowser.open_new_tab(url_short)

    if has_error:
        sys.exit(1)
