# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['djangocms_calameo', 'djangocms_calameo.migrations']

package_data = \
{'': ['*'],
 'djangocms_calameo': ['locale/fr/LC_MESSAGES/*',
                       'templates/djangocms_calameo/*']}

install_requires = \
['Django>=1.8,<3', 'django-cms>=3.4,<4.0']

setup_kwargs = {
    'name': 'djangocms-calameo',
    'version': '2.0.1',
    'description': 'Django CMS Calaméo is a plugin for Django CMS that allows you to add Calaméo widgets on your site.',
    'long_description': '# djangocms-calameo\n\n**Django CMS Calaméo** is a plugin for [Django CMS](http://django-cms.org/) that allows you to add Calaméo widgets on your site.\n\n![](preview.png)\n\n# Installation\n\n- run `pip install djangocms-calameo`\n- add `djangocms_calameo` to your `INSTALLED_APPS`\n- run `python manage.py migrate djangocms_calameo`\n\n# Known issues\n\nA [bug in Firefox](https://bugzilla.mozilla.org/show_bug.cgi?id=1459147) prevents the iframe to reload with new parameters.\nYou must force reload the page after saving the plugin.\n',
    'author': 'Kapt dev team',
    'author_email': 'dev@kapt.mobi',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/kapt/open-source/djangocms-calameo',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, !=3.5.*, !=3.6.*, !=3.7.*',
}


setup(**setup_kwargs)
