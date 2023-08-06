from uuid import UUID

from .base import BaseClient


class UserClient(BaseClient):
    """
    Everything related to both account types
    """
    def accounts_get(
        self,
        account_id: str = None,
        username: str = None,
        account_type: str = None,
        country: str = None,
        email: str = None,
        first_name: str = None,
        last_name: str = None,
        is_powerseller: bool = None,
        not_blocked: bool = None,
        params: {} = None,
        **kwargs
    ):
        """
        :account_id: Only available to accounts with the UserAdmin role
        :username: Available to everyone
        :account_type: Available to everyone (Private, Business)
        :country: ISO-3166 ALPHA-2 (D == DE)
        :email: Only available to accounts with the UserAdmin role
        :first_name: Only available to accounts with the UserAdmin role
        :last_name: Only available to accounts with the UserAdmin role
        :is_powerseller: Available to everyone
        :not_blocked: Only available to accounts with the UserAdmin role

        :params: Custom GET parameters
        """

        params = params or {}
        if account_id is not None:
            params.setdefault('accountId', account_id)
        if username is not None:
            params.setdefault('username', username)
        if account_type is not None:
            params.setdefault('accountType', account_type)
        if country is not None:
            params.setdefault('country', country)
        if email is not None:
            params.setdefault('email', email)
        if first_name is not None:
            params.setdefault('firstName', first_name)
        if last_name is not None:
            params.setdefault('lastName', last_name)
        if is_powerseller is not None:
            params.setdefault('isPowerseller', is_powerseller)
        if not_blocked is not None:
            params.setdefault('notBlocked', not_blocked)

        return self._request(
            'GET',
            'accounts',
            params=params,
            **kwargs
        )

    def accounts_post(
        self,
        id: UUID = None,
        first_name: str = None,
        last_name: str = None,
        enable_english_product_names: bool = None,
        display_language_id: str = None,
        email_language_id: str = None,
        addresses: dict = None,
        is_powerseller: bool = None,
        homepage_layout: str = None,
        data: {} = None,
        **kwargs,
    ):
        """
        :id: An auto generated uuid used to identify the object.
        :first_name: pattern: /^[^;<>=]{2,25}$/
        :last_name: pattern: /^[^;<>=]{2,40}$/
        :enable_english_product_names: Determines, if product names are shown in English
         instead of the users standard language.
        :display_language_id: ISO-3166 ALPHA-2 (D == DE)
        :email_language_id: ISO-3166 ALPHA-2 (D == DE)
        :addresses: Address objects referenced by UUID in a dictionary
        :is_powerseller: A flag that marks a seller as particularly outstanding
        :homepage_layout: home page layout  # TODO Describe

        :data: Custom POST data
        """
        data = data or {}
        if id is not None:
            data.setdefault('id', id)
        if first_name is not None:
            data.setdefault('firstName', first_name)
        if last_name is not None:
            data.setdefault('lastName', last_name)
        if enable_english_product_names is not None:
            data.setdefault('enableEnglishProductNames', enable_english_product_names)
        if display_language_id is not None:
            data.setdefault('displayLanguageId', display_language_id)
        if email_language_id is not None:
            data.setdefault('emailLanguageId', email_language_id)
        if addresses is not None:
            data.setdefault('addresses', addresses)
        if is_powerseller is not None:
            data.setdefault('isPowerseller', is_powerseller)
        if homepage_layout is not None:
            data.setdefault('homepageLayout', homepage_layout)

        return self._request(
            'POST',
            'accounts',
            data=data,
            **kwargs
        )

    def account_get(
        self,
        id: UUID,
        min_version: int = None,
        params: {} = None,
        **kwargs,
    ):
        """

        :id: An auto generated uuid used to identify the object

        :min_version:

        :params: Custom get params
        """
        params = params or {}
        if min_version is not None:
            params.setdefault('min_version', min_version)
        return self._request(
            'GET',
            f'accounts/{id}',
            params=params,
            **kwargs
        )
