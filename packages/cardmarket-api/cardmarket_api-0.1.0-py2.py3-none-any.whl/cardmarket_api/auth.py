from oauthlib.oauth2 import is_secure_transport, InsecureTransportError
from requests_oauthlib import OAuth2


class Auth(OAuth2):
    def __init__(self, client_id=None, client=None, token=None):
        """Construct a new OAuth 2 authorization object.
        """
        super(Auth, self).__init__(client_id, client, token)

    def __call__(self, r):
        """Append an OAuth 2 token to the _request.
        """
        if not is_secure_transport(r.url):
            raise InsecureTransportError()
        r.headers.__setitem__("Authorization", self._client.id_token)
        return r
