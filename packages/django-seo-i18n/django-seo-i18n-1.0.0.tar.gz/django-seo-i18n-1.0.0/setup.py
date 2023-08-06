#!/usr/bin/env python
from setuptools import setup

from seo_i18n import VERSION

setup(
    name='django-seo-i18n',
    version=VERSION,
    description='SEO functionality for any object or custom URL with multilingual support',
    long_description=open('README.md').read(),
    author='Pragmatic Mates',
    author_email='info@pragmaticmates.com',
    maintainer='Pragmatic Mates',
    maintainer_email='info@pragmaticmates.com',
    url='https://github.com/PragmaticMates/django-seo-i18n',
    packages=[
        'seo_i18n',
        'seo_i18n.migrations',
        'seo_i18n.templatetags'
    ],
    include_package_data=True,
    install_requires=('django', 'django-modeltrans'),
    classifiers=[
        'Programming Language :: Python',
        'Operating System :: OS Independent',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Framework :: Django',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Development Status :: 5 - Production/Stable'
    ],
    license='LGPLv3',
    keywords="django seo fields URL i18n multilingual",
)
