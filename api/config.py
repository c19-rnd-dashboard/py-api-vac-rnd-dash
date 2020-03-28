import pathlib
from decouple import config

PACKAGE_ROOT = pathlib.Path(__file__).resolve().parent.parent

with open(PACKAGE_ROOT / "VERSION") as version_file:
    __version__ = version_file.read().strip()


class Config:
    pass


class DevelopmentConfig(Config):
    pass
