import pathlib
from decouple import config

PACKAGE_ROOT = pathlib.Path(__file__).resolve().parent.parent

with open(PACKAGE_ROOT / "VERSION") as version_file:
    __version__ = version_file.read().strip()


class Config:
    CRED_PATH = PACKAGE_ROOT + "credentials.json"
    # If modifying these scopes, delete the file token.pickle.
    SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
    SPREADSHEET_ID = "1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms"
    RANGE_NAME = "Class Data!A2:E"


class DevelopmentConfig(Config):
    pass
