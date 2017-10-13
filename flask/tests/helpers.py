
from base64 import b64encode


def make_auth_header(username, password):
    return 'Basic ' + b64encode('{0}:{1}'.format(username, password).encode('utf-8')).decode()
