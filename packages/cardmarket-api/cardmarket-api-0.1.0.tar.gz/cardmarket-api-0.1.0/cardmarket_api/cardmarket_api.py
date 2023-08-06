import boto3

from .auth import Auth
from . import clients

DOMAIN_MAPPING = {
    'global': 'https://global{stage}.cardmarket.com/v3',
    'user': 'https://user{stage}.cardmarket.com/v3',
    'product': 'https://product{stage}.cardmarket.com/v3',
    'marketplace': 'https://marketplace{stage}.cardmarket.com/v3',
}


class CardMarketApi:
    def __init__(
        self,
        auth: Auth = None,
        username: str = None,
        password: str = None,
        client_id: str = '15kh0e0f04o1iaq5ie8jf78fuh',
        aws_region: str = 'eu-central-1',
        sandbox=False,
    ):
        """
        :sandbox: Sandbox mode vs Production
        """
        self.sandbox = sandbox
        if not auth:
            self.auth = self.build_auth(aws_region, client_id, username, password)
        else:
            self.auth = auth
        self.global_client = clients.GlobalClient(
            base_endpoint=DOMAIN_MAPPING['global'].format(
                stage='.sandbox' if sandbox else ''
            ),
            auth=self.auth
        )
        self.user = clients.UserClient(
            base_endpoint=DOMAIN_MAPPING['user'].format(
                stage='.sandbox' if sandbox else ''
            ),
            auth=self.auth,
        )
        self.product = clients.ProductClient(
            base_endpoint=DOMAIN_MAPPING['product'].format(
                stage='.sandbox' if sandbox else ''
            ),
            auth=self.auth,
        )
        self.marketplace = clients.MarketplaceClient(
            base_endpoint=DOMAIN_MAPPING['marketplace'].format(
                stage='.sandbox' if sandbox else ''
            ),
            auth=self.auth,
        )
        super(CardMarketApi, self).__init__()

    def build_auth(self, aws_region, client_id, username, password):
        client = boto3.client('cognito-idp', region_name=aws_region)
        response = client.initiate_auth(
            ClientId=client_id,
            AuthFlow='USER_PASSWORD_AUTH',
            AuthParameters={
                'USERNAME': username,
                'PASSWORD': password
            }
        )
        assert response['ResponseMetadata']['HTTPStatusCode'] == 200, "Authentication failed"
        result = response['AuthenticationResult']
        return Auth(
            client_id=client_id,
            token={
                # 'token_type': result['TokenType'],
                # 'access_token': result['AccessToken'],
                # 'refresh_token': result['RefreshToken'],
                # 'expires': result['ExpiresIn'],
                'id_token': result['IdToken']
            }
        )
