from requests import HTTPError


class ApiException(HTTPError):
    # TODO custom logic for different error types
    pass
