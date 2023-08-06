**Django SSL Support**
###### SSL SMTP email backend for Django Web Framework
------------
**Version: 1.1.0**
------------
[![Django](https://static.djangoproject.com/img/logos/django-logo-negative.png "Django")](https://djangoproject.com "Django")

[![SMTP](https://mailtrap.io/wp-content/uploads/2019/10/use-port-number-1.png "SMTP")](https://himelrana.com "SMTP")

------------
Installation
------------
`pip install django-ssl-smtp`

and add following to your ``settings.py``:


    EMAIL_BACKEND = 'django_ssl_smtp.SSLEmailBackend'
    EMAIL_HOST = 'mail.example.com'
    EMAIL_PORT = 465
    DEFAULT_FROM_EMAIL = user@example.com 
> **DEFAULT_FROM_EMAIL **	 is optional, But most of the ssl 	smtp do not allow random sender name.

For any kind of bug or update. Request to `contact@himelrana.com`
