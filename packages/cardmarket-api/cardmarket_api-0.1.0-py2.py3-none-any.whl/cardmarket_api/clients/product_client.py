from .base import BaseClient


class ProductClient(BaseClient):
    """
    Manage product aggregates.
    """
    def products_get(
        self,
        **kwargs
    ):
        """
        No parameters
        """
        return self._request(
            'GET',
            'products',
            **kwargs,
        )

    def products_post(
        self,
        id: str = None,
        name: str = None,
        length: int = None,
        width: int = None,
        height: int = None,
        weight: int = None,
        description: str = None,
        is_active: bool = True,
        release_date: str = None,
        product_image: str = None,
        category_id: str = None,
        values: dict = None,
        data: dict = None,
        **kwargs
    ):
        """
        :id: An auto generated uuid used to identify the object.
        :name: pattern: ^[a-zA-Z0-9 ]+$, max_length=25, required
        :length: The length of the product in millimetres (mm), required
        :width: The width of the product in millimetres (mm), required
        :height: The height of the product in millimetres (mm), required
        :weight: The weight of the object in grams (g), required
        :description: max_length: 255
        :is_active: default true
        :release_date: example: 1970-01-31
        :product_image:
        :category_id: uuid, required
        :values: ProductAttributeValue objects referenced by UUID in a dictionary
        """

        data = data or {}
        if id is not None:
            data.setdefault('id', id)
        if name is not None:
            data.setdefault('name', name)
        if length is not None:
            data.setdefault('length', length)
        if width is not None:
            data.setdefault('width', width)
        if height is not None:
            data.setdefault('height', height)
        if weight is not None:
            data.setdefault('weight', weight)
        if description is not None:
            data.setdefault('description', description)
        if is_active is not None:
            data.setdefault('isActive', is_active)
        if release_date is not None:
            data.setdefault('releaseDate', release_date)
        if product_image is not None:
            data.setdefault('productImage', product_image)
        if category_id is not None:
            data.setdefault('categoryId', category_id)
        if values is not None:
            data.setdefault('values', values)

        return self._request(
            'POST',
            'products',
            data=data,
            **kwargs
        )

    # TODO product detail

    def categories_get(
        self,
        **kwargs,
    ):
        """
        No parameters
        """
        return self._request(
            'GET',
            'categories',
            **kwargs
        )
