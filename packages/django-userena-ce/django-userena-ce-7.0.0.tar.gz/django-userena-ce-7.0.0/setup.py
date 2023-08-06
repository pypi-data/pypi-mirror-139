# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['userena',
 'userena.contrib',
 'userena.contrib.umessages',
 'userena.contrib.umessages.migrations',
 'userena.contrib.umessages.templatetags',
 'userena.contrib.umessages.tests',
 'userena.management',
 'userena.management.commands',
 'userena.migrations',
 'userena.runtests',
 'userena.tests',
 'userena.tests.profiles']

package_data = \
{'': ['*'],
 'userena': ['fixtures/*',
             'locale/ar/LC_MESSAGES/*',
             'locale/bg/LC_MESSAGES/*',
             'locale/de/LC_MESSAGES/*',
             'locale/de_du/LC_MESSAGES/*',
             'locale/el/LC_MESSAGES/*',
             'locale/es/LC_MESSAGES/*',
             'locale/fr/LC_MESSAGES/*',
             'locale/gl/LC_MESSAGES/*',
             'locale/it/LC_MESSAGES/*',
             'locale/nb/LC_MESSAGES/*',
             'locale/nl/LC_MESSAGES/*',
             'locale/pl/LC_MESSAGES/*',
             'locale/pt/LC_MESSAGES/*',
             'locale/pt_BR/LC_MESSAGES/*',
             'locale/ro/LC_MESSAGES/*',
             'locale/ru/LC_MESSAGES/*',
             'locale/tr/LC_MESSAGES/*',
             'locale/zh_Hans/LC_MESSAGES/*',
             'locale/zh_Hant/LC_MESSAGES/*',
             'templates/*',
             'templates/userena/*',
             'templates/userena/emails/*'],
 'userena.contrib.umessages': ['fixtures/*',
                               'templates/*',
                               'templates/umessages/*'],
 'userena.runtests': ['private/*', 'templates/*']}

install_requires = \
['Django>=3.2,<5.0', 'django-guardian>=2.0', 'easy-thumbnails', 'html2text']

setup_kwargs = {
    'name': 'django-userena-ce',
    'version': '7.0.0',
    'description': 'Complete user management application for Django',
    'long_description': "# Django Userena (Community Edition)\n\n[![Build Status](https://github.com/django-userena-ce/django-userena-ce/workflows/CI/badge.svg)](https://github.com/django-userena-ce/django-userena-ce/actions?query=workflow%3ACI+branch%3Amaster)\n[![PyPI version](https://badge.fury.io/py/django-userena-ce.svg)](https://badge.fury.io/py/django-userena-ce)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/django-userena-ce)](https://pypi.org/project/django-userena-ce/)\n[![Coverage Status](https://coveralls.io/repos/github/django-userena-ce/django-userena-ce/badge.svg?branch=master)](https://coveralls.io/github/django-userena-ce/django-userena-ce?branch=master)\n[![Documentation Status](https://img.shields.io/badge/docs-passing-4a4c4c1.svg)](https://django-userena-ce.github.io/django-userena-ce/)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\nThis project is a community edition fork of\n[django-userena](https://github.com/bread-and-pepper/django-userena).\n\nUserena is a Django application that supplies your Django project with full\naccount management. It's a fully customizable application that takes care of\nthe signup, activation, messaging and more. It's BSD licensed, which means you\ncan use it commercially for free!\n\n## Supported Software\n\nSoftware | Versions\n---|---\nPython | 3.7, 3.8, 3.9, 3.10\nDjango | 3.2, 4.0\nDjango Guardian | \\>2.0\n\n## [Documentation](https://django-userena-ce.github.io/django-userena-ce/index.html)\n\nComplete documentation about the\n[installation](https://django-userena-ce.github.io/django-userena-ce/installation.html),\n[settings](https://django-userena-ce.github.io/django-userena-ce/settings.html) and\n[F.A.Q.](https://django-userena-ce.github.io/django-userena-ce/faq.html) is available on\n[All Documentation](https://django-userena-ce.github.io/django-userena-ce/index.html).\n\nFor list of updates and changes see `HISTORY.md` file.\n",
    'author': 'James Meakin',
    'author_email': 'django-userena-ce@jmsmkn.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/django-userena-ce/django-userena-ce',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<3.11',
}


setup(**setup_kwargs)
