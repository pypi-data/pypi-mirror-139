# djangocms-calameo

**Django CMS Calaméo** is a plugin for [Django CMS](http://django-cms.org/) that allows you to add Calaméo widgets on your site.

![](preview.png)

# Installation

- run `pip install djangocms-calameo`
- add `djangocms_calameo` to your `INSTALLED_APPS`
- run `python manage.py migrate djangocms_calameo`

# Known issues

A [bug in Firefox](https://bugzilla.mozilla.org/show_bug.cgi?id=1459147) prevents the iframe to reload with new parameters.
You must force reload the page after saving the plugin.
