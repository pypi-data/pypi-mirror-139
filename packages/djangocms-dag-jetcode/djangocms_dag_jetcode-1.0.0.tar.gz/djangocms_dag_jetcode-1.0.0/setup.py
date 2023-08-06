# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['djangocms_dag_jetcode',
 'djangocms_dag_jetcode.conf',
 'djangocms_dag_jetcode.migrations']

package_data = \
{'': ['*'],
 'djangocms_dag_jetcode': ['locale/fr/LC_MESSAGES/*',
                           'static/djangocms_dag_jetcode/css/*',
                           'static/djangocms_dag_jetcode/img/*',
                           'templates/djangocms_dag_jetcode/*']}

install_requires = \
['Django>=2.0,<3.0',
 'django-cms>=3.8.0,<4.0.0',
 'django-multiselectfield>=0.1.12,<0.2.0',
 'djangocms-attributes-field>=2.0.0,<3.0.0']

setup_kwargs = {
    'name': 'djangocms-dag-jetcode',
    'version': '1.0.0',
    'description': '',
    'long_description': None,
    'author': 'Kapt dev team',
    'author_email': 'dev@kapt.mobi',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
