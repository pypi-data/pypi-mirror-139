from .base import BaseClient


class GlobalClient(BaseClient):

    def retrieve_token_post(
        self,
        username: str = None,
        password: str = None,
        data: dict = None,
        **kwargs
    ):
        """
        Endpoint that allows the user to retrieve an access token for their account.
        """

        data = data or {}
        if username is not None:
            data.setdefault('username', username)
        if password is not None:
            data.setdefault('password', password)

        return self._request(
            'POST',
            'RetrieveToken',
            data=data,
            **kwargs,
        )
