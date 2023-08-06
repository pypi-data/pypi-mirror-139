Cardmakret API v3+
==================

|pypi|

|travis ci|

|Documentation Status|

Python client for CardMarket API v3+

-  Free software: MIT license
-  Documentation: https://cardmarket-api.readthedocs.io.

Features
--------

Python client wrapping HTTP calls to ``Cardmarket API v3+``

Installation
------------
   .. code:: shell

        $ pip install cardmarket-api


Usage
-----
   .. code:: python

        from cardmarket_api import CardMarketApi

        api = CardMarketApi(
            username='username',
            password='password',
            sandbox=True,
        )

        # User
        ## Get Users
        api.user.accounts_get()

        ## Create user profile
        api.user.accounts_post(
            first_name='John',
            last_name='Travolta',
            enable_english_product_names=True,
            is_powerseller=True,
        )


        # Product
        ## List products
        api.product.products_get()


        # Marketplace
        ## List articles in marketplace
        api.marketplace.articles_get()

Credits
-------

This package was created with
`Cookiecutter <https://github.com/audreyr/cookiecutter>`__ and the
`audreyr/cookiecutter-pypackage <https://github.com/audreyr/cookiecutter-pypackage>`__
project template.

.. |pypi| image:: https://img.shields.io/pypi/v/cardmarket-api.svg
   :target: https://pypi.python.org/pypi/cardmarket_api
.. |travis ci| image:: https://img.shields.io/travis/SukiCZ/cardmarket-api.svg
   :target: https://travis-ci.com/SukiCZ/cardmarket_api
.. |Documentation Status| image:: https://readthedocs.org/projects/cardmarket-api/badge/?version=latest
   :target: https://cardmarket-api.readthedocs.io/en/latest/?version=latest
