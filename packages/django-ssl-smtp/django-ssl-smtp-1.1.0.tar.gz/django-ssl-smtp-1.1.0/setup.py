from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Framework :: Django',
  'Intended Audience :: Developers',
  'Operating System :: OS Independent',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3',
  'Topic :: Software Development :: Libraries :: Python Modules',
]
setup(
  name='django-ssl-smtp',
  version='1.1.0',
  description='SSL SMTP Support for Django Framework 4.0 and UP',
  long_description=open('README.md').read() + '\n\n' + open('CHANGELOG.txt').read(),
  long_description_content_type='text/markdown',
  url='https://himelrana.com',  
  author='Himel',
  author_email='contact@himelrana.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='django, smtp, ssl smtp, smtp ssl, django ssl smtp, django smtp ssl, ssl', 
  packages=find_packages(),
  python_requires='>=3.6',
  install_requires=[] 
)