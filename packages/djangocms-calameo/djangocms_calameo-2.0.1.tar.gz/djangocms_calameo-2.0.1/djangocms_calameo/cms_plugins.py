# -*- coding:utf-8 -*-
from __future__ import unicode_literals

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.translation import ugettext as _, ugettext_lazy

from .models import Publication


@plugin_pool.register_plugin
class PublicationPlugin(CMSPluginBase):
    module = ugettext_lazy("Widgets")
    name = ugettext_lazy("Calaméo publication widget")
    model = Publication
    render_template = "djangocms_calameo/default.html"
    cache = False

    def get_fieldsets(self, request, obj):
        fieldsets = (
            (None, {"fields": ["title", "url"]}),
            (
                _("More options"),
                {
                    "classes": ("collapse",),
                    "fields": [
                        "mode",
                        "view",
                        "size",
                        "default_page",
                        "actions",
                        "must_open_in_new_window",
                        "must_show_share_menu",
                        "must_show_book_title",
                        "must_auto_flip",
                    ],
                },
            ),
        )

        return fieldsets
