from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("lain_shorten")
except PackageNotFoundError:
    __version__ = "dev"
