# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['drf_actions',
 'drf_actions.migrations',
 'drf_actions.serializers',
 'drf_actions.views']

package_data = \
{'': ['*']}

install_requires = \
['Django>3.1.6',
 'django-filter>=2.4.0',
 'django-model-utils>=4.1.1',
 'djangorestframework>=3.12.2']

setup_kwargs = {
    'name': 'drf-actions',
    'version': '0.2.1',
    'description': 'Create event log with help triggers and send notify after create event',
    'long_description': '# drf-actions\n\nCreate event log with help triggers and send notify after create event\n',
    'author': 'Pavel Maltsev',
    'author_email': 'pavel@speechki.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/speechki-book/drf-actions',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
