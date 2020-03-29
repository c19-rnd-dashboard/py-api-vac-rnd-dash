import pathlib
from decouple import config
import os

PACKAGE_ROOT = pathlib.Path(__file__).resolve().parent.parent

with open(PACKAGE_ROOT / "VERSION") as version_file:
    __version__ = version_file.read().strip()


class Config:
    if os.path.isfile(os.path.join(PACKAGE_ROOT, "credentials.json")):
        CRED_PATH = os.path.join(PACKAGE_ROOT, "credentials.json")
    # If modifying these scopes, delete the file token.pickle.
    SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
    SPREADSHEET_ID = "1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms"
    RANGE_NAME = "Class Data!A2:E"


class DevelopmentConfig(Config):
    pass

# Setup requirements for local environment
def local_setup():
    raise NotImplemented