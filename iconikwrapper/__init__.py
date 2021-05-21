#import os
import requests


app_id = os.environ.get('app_id', None)
token = os.environ.get('token', None)


class APIKeyMissingError(Exception):
    pass

if app_id is None:
    raise APIKeyMissingError(
        "All methods require an API app id"
    )
elif token is None:
    raise APIKeyMissingError(
        "All methods require an API auth token."
    )


session = requests.Session()
session.headers = {}
session.headers['App-ID'] = app_id
session.headers['Auth-Token'] = token


from .iconik import assets
from .iconik import users
from .iconik import jobs
