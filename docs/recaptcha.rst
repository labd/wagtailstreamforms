Enabling reCAPTCHA
==================

Has been enabled via the `django-recaptcha <https://github.com/praekelt/django-recaptcha>`_ package.

Once you have `signed up for reCAPTCHA <https://www.google.com/recaptcha/intro/index.html>`_.

Follow the below and an option will be in the form setup ``fields`` tab to add a reCAPTCHA.

Just add ``captcha`` to your ``INSTALLED_APPS`` settings:

.. code-block:: python

    INSTALLED_APPS = [
        ...
        'captcha'
        ...
    ]

Add the required keys in your settings:

.. code-block:: python

    RECAPTCHA_PUBLIC_KEY = 'xxx'
    RECAPTCHA_PRIVATE_KEY = 'xxx'

If you would like to use the new No Captcha reCaptcha add the setting ``NOCAPTCHA = True``. For example:

.. code-block:: python

    NOCAPTCHA = True
