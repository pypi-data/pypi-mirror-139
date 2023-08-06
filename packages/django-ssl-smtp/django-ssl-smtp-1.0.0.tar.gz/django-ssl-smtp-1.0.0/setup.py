from distutils.core import setup

setup(
    name='django-ssl-smtp',
    version='1.0.0',
    description='SSL SMTP Support for Django Framework 4.0 and UP',
    author='Himel',
    author_email='contact@himelrana.com',
    url='https://himelrana.com',
    license='MIT',
    py_modules=('django_ssl_smtp',),
    zip_safe=True,
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)