# -*- coding: utf-8 -*-
from cms.models.pluginmodel import CMSPlugin
from django.db import models
from django.http import QueryDict
from django.utils.translation import pgettext_lazy, ugettext_lazy
from future.utils import python_2_unicode_compatible


@python_2_unicode_compatible
class Publication(CMSPlugin):
    title = models.CharField(verbose_name=ugettext_lazy("Title"), max_length=250)
    url = models.URLField(
        verbose_name=ugettext_lazy("URL"),
        help_text=ugettext_lazy("The URL of the publication"),
    )

    MODE_CHOICES = (
        ("mini", ugettext_lazy("Mini")),
        ("viewer", pgettext_lazy("like a book", "Publication")),
    )
    mode = models.CharField(
        verbose_name=ugettext_lazy("Mode"),
        choices=MODE_CHOICES,
        max_length=6,
        default=MODE_CHOICES[0][0],
    )

    VIEW_CHOICES = (
        ("", ugettext_lazy("Auto")),
        ("book", pgettext_lazy("noun", "Book")),
        ("slide", ugettext_lazy("Slide")),
        ("scroll", ugettext_lazy("Scroll")),
    )
    view = models.CharField(
        verbose_name=ugettext_lazy("View"),
        choices=VIEW_CHOICES,
        max_length=6,
        blank=True,
        default=VIEW_CHOICES[0][0],
    )

    SIZE_CHOICES = (
        ("small", ugettext_lazy("Small")),
        ("medium", ugettext_lazy("Medium")),
        ("big", ugettext_lazy("Big")),
        ("full", ugettext_lazy("Full")),
    )
    size = models.CharField(
        verbose_name=ugettext_lazy("Size"),
        choices=SIZE_CHOICES,
        max_length=6,
        default=SIZE_CHOICES[1][0],
    )

    default_page = models.IntegerField(
        verbose_name=ugettext_lazy("Default page"),
        default=1,
        help_text=ugettext_lazy("Enter the page number to display by default"),
    )

    ACTIONS_CHOICES = (
        ("embed", ugettext_lazy("Open publication in full screen directly")),
        ("public", ugettext_lazy("Open description page")),
        ("view", ugettext_lazy("Open viewer directly")),
    )
    actions = models.CharField(
        verbose_name=ugettext_lazy("Actions"),
        choices=ACTIONS_CHOICES,
        max_length=6,
        default=ACTIONS_CHOICES[0][0],
    )

    must_open_in_new_window = models.BooleanField(
        ugettext_lazy("Open in new window"), default=True
    )
    must_show_share_menu = models.BooleanField(
        ugettext_lazy("Show the sharing menu after reading"), default=True
    )
    must_show_book_title = models.BooleanField(
        ugettext_lazy("Display the publication title"), default=True
    )
    must_auto_flip = models.BooleanField(
        ugettext_lazy("Automatically turn pages"), default=False
    )

    class Meta:
        verbose_name = ugettext_lazy("Publication")
        verbose_name_plural = ugettext_lazy("Publications")

    def __str__(self):
        return self.title

    @property
    def code(self):
        "Return the publication code parsed from the URL"
        return self.url.rstrip("/").split("/")[-1]

    def get_size(self):
        if self.size == self.SIZE_CHOICES[0][0]:
            return {"width": "400", "height": "250"}
        elif self.size == self.SIZE_CHOICES[1][0]:
            return {"width": "480", "height": "300"}
        elif self.size == self.SIZE_CHOICES[2][0]:
            return {"width": "560", "height": "350"}
        else:
            return {"width": "100%", "height": "100%"}

    def get_parameters(self):
        parameters = QueryDict(mutable=True)
        parameters["bkcode"] = self.code
        parameters["mode"] = self.mode
        if self.view != "":
            parameters["view"] = self.view
        parameters["page"] = self.default_page
        parameters["clickto"] = self.actions
        parameters["clicktarget"] = (
            "_blank" if self.must_open_in_new_window else "_self"
        )
        parameters["showsharemenu"] = self.must_show_share_menu
        if self.must_auto_flip:
            parameters["autoflip"] = 4

        return parameters.urlencode()
