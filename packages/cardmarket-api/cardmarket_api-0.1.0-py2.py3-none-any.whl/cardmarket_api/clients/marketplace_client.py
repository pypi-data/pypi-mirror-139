from uuid import UUID

from .base import BaseClient


class MarketplaceClient(BaseClient):
    """
    Endpoints used to manage your inventory on Cardmarket
    """
    def articles_get(
        self,
        account_id: UUID = None,
        product_id: UUID = None,
        binder_id: UUID = None,
        in_shopping_cart: bool = None,
        params: dict = None,
        **kwargs
    ):
        """
        :account_id: Only available to Marketplace and Super admins.
        :product_id: An auto generated uuid used to identify the object.
        :binder_id:
        :in_shopping_cart:
        """

        params = params or {}
        if account_id is not None:
            params.setdefault('accountId', account_id)
        if product_id is not None:
            params.setdefault('productId', product_id)
        if binder_id is not None:
            params.setdefault('binderId', binder_id)
        if in_shopping_cart is not None:
            params.setdefault('inShoppingCart', in_shopping_cart)

        return self._request(
            'GET',
            'inventory/articles',
            params=params,
            **kwargs,
        )
