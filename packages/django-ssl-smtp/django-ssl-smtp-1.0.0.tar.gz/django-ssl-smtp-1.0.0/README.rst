django-ssl-smtp
===============

SSL SMTP email backend for Django Web Framework

**NOTE: Django 4.0 >= includes support for SMTP with SSL/TLS


Installation
------------

Run

::

    pip install django-ssl-smtp


and add following to your ``settings.py``:

::

    EMAIL_BACKEND = 'django_ssl_smtp.SSLEmailBackend'
    EMAIL_HOST = 'mail.example.com'
    EMAIL_PORT = 465
    DEFAULT_FROM_EMAIL = user@example.com # This is optional, But most of the ssl smtp don't not allow random sender name.
