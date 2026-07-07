# lain-shorten

A simple CLI URL shortener for multiple url-shortening services, with optional clipboard copy.

## Installation

### Via PyPI (Recommended)

You have the option to choose between the standard version (`lain-shorten`) or the desktop version (`lain-shorten[clipboard]`), which adds clipboard support for auto-copying links.

> [!NOTE]
> For brevity, the examples below use the desktop version.

#### With pip (Basic)

```sh
pip install "lain-shorten[clipboard]"
```

#### With pipx (Isolated)

```sh
pipx install "lain-shorten[clipboard]"
```

#### With uv (Best)

The most efficient way to install or run `lain-shorten`.

```sh
# Permanent isolated installation
uv tool install "lain-shorten[clipboard]"

# Run once without installing
uvx --with "lain-shorten[clipboard]" lain-shorten <url1> <url2> <url3>

# Run in scripts or ad-hoc environments
uv run --with "lain-shorten[clipboard]" lain-shorten <url1> <url2> <url3>
```

### From Source (Development)

```sh
# Clone the repository and navigate to it
git clone git@github.com:NecRaul/lain-shorten.git
cd lain-shorten

# Install environment and all development dependencies (mandatory and optional)
uv sync --dev

# Install pre-commit hook
uv run pre-commit install

# Optional: Run all linters and type checkers manually
uv run pre-commit run --all-files

# Run the local version
uv run lain-shorten <url1> <url2> <url3>

# Run tests
uv run pytest tests
```

## Usage

Simply provide a URL, and the tool will automatically handle protocol validation and formatting.

Use `--open` to open each generated short URL in your default browser right after shortening. This makes it easy to verify each link resolves as expected in a real browser session.

```sh
# Shorten a URL (default shortener: lainla)
lain-shorten https://kuroneko.dev

# Protocol-less (automatically prepends http://)
lain-shorten kuroneko.dev

# Select a specific shortener
lain-shorten --shortener wildlain https://github.com/NecRaul

# Shorten using every available shortener
lain-shorten --shortener all https://gist.github.com/NecRaul

# irc
lain-shorten irc://irc.libera.chat/#archlinux

# ssh
lain-shorten ssh://necraul@kuroneko.dev

# mailto
lain-shorten mailto:necraul@kuroneko.dev

# sms
lain-shorten sms:+15551234567

# magnet torrent
lain-shorten "magnet:?xt=urn:btih:0123456789abcdef0123456789abcdef01234567&dn=Example"

# Open shortened URLs using the default browser
lain-shorten --open \
    http://kuroneko.dev \
    ircs://irc.libera.chat:6697/#archlinux \
    xmpp:necraul@kuroneko.dev \
    tel:+15551234567

# Display help and version
lain-shorten -h
lain-shorten -v
```

### Options

```sh
    --shortener       SHORTENER             URL shortening service to use (default: lainla)
    --open            -                     Open each shortened URL in your default browser after shortening
    --config          PATH                  Path to a custom configuration file
    --init-config     [PATH]                Create a default configuration file at the default or given path
    --show-config     -                     Print the effective configuration after merging defaults and config file
    --no-config       -                     Ignore the configuration file and use only CLI flags
-h, --help            -                     Show help and exit
-v, --version         -                     Show version and exit
```

### Configuration

`lain-shorten` supports a JSON configuration file to set a default shortener and whether to open shortened URLs in your browser. You can create a default config, inspect the effective configuration, and override or ignore the config file at runtime.

- Default path
  - Linux/BSD: `$XDG_CONFIG_HOME/necraul/lain-shorten.json` or `~/.config/necraul/lain-shorten.json`
  - MacOS: `~/Library/Application Support/necraul/lain-shorten.json`
  - Windows: `%APPDATA%/necraul/lain-shorten.json`
- Basic structure
  - `default_shortener`: shortener used when `--shortener` flag is omitted (default: `"lainla"`).
  - `open_urls`: whether to open each generated short URL in your default browser (default: `false`).

```json
{
  "default_shortener": "lainla",
  "open_urls": false
}
```

```sh
# Create a default configuration file at the default path
lain-shorten --init-config

# Create a default configuration file at a custom path
lain-shorten --init-config config.json

# Show the effective configuration (defaults merged with the default config file)
lain-shorten --show-config

# Create a default configuration file at the default path and print it
lain-shorten --init-config --show-config

# Create a default configuration file at a custom path and print it
lain-shorten --init-config /path/to/config.json --show-config

# Show the effective configuration (defaults merged with the custom config file)
lain-shorten --config config.json --show-config

# Shorten URLs using the config file's default_shortener (no --shortener needed)
lain-shorten https://kuroneko.dev/

# Override the config file's default_shortener
lain-shorten --shortener wildlain https://github.com/NecRaul

# Use a custom configuration file
lain-shorten --config /path/to/config.json https://gist.github.com/NecRaul

# Ignore the configuration file and use only CLI flags
lain-shorten --no-config https://kuroneko.dev/

# Open shortened URLs in your browser (CLI flag overrides config)
lain-shorten --open https://github.com/NecRaul/
```

## Supported Shorteners

- [s.lain.la](https://s.lain.la/)
- [s.wildla.in](https://s.wildla.in/)
- [v.gd](https://v.gd/)
- [1pt.co](https://1pt.co/)

## Supported Schemes

- `http://` and `https://` links.
- Protocol-less domains (automatically normalized to `http://`).
- `irc://` and `ircs://` links.
- `ssh://` links.
- `mailto://` and `xmpp://` links.
- `sms://` and `tel://` links.
- `magnet:` torrent links.

## Dependencies

- [requests](https://github.com/psf/requests): send the API request for shortening.

### Optional

- [pyperclip](https://github.com/asweigart/pyperclip): copy the shortened URLs to the clipboard.

## How it works

Supported services allow shortening URLs via an `HTTP` request.

This tool automates the process to avoid typing long `curl` strings.

### The Manual Way

```sh
curl -d "url=https://kuroneko.dev" https://s.lain.la
```

### The lain-shorten way

- Batch Processing: Shorten multiple URLs in a single command, iterating through each one and printing results as they come in rather than waiting for the entire batch to finish.
- Validation: Uses `urllib` to parse and validate each URL before sending it, catching malformed input early and normalizing protocol-less domains to `http://` so the request always reaches the service in a well-formed state.
- API Request: Sends an `HTTP` request via `requests`, then reads the plain-text or JSON response depending on the service.
- Normalization: Extracts a clean short URL from whatever format the service returns so the output is consistent across different shorteners.
- Clipboard (Optional): If `pyperclip` is installed, each resulting URL is copied to the clipboard immediately after shortening so it is ready to paste without any extra steps.

## Special thanks

- To **7666** of <https://lain.la/> for running the [shortener](https://s.lain.la/) service that inspired this project.
