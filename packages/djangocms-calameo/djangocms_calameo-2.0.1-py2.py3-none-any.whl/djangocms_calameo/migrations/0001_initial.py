# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cms", "0016_auto_20160608_1535"),
    ]

    operations = [
        migrations.CreateModel(
            name="Publication",
            fields=[
                (
                    "cmsplugin_ptr",
                    models.OneToOneField(
                        parent_link=True,
                        related_name="djangocms_calameo_publication",
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        on_delete=models.CASCADE,
                        to="cms.CMSPlugin",
                    ),
                ),
                ("title", models.CharField(max_length=250, verbose_name="Title")),
                (
                    "url",
                    models.URLField(
                        help_text="The URL of the publication", verbose_name="URL"
                    ),
                ),
                (
                    "mode",
                    models.CharField(
                        default=b"mini",
                        max_length=6,
                        verbose_name="Mode",
                        choices=[(b"mini", "Mini"), (b"viewer", "Publication")],
                    ),
                ),
                (
                    "view",
                    models.CharField(
                        default=b"",
                        max_length=6,
                        verbose_name="View",
                        blank=True,
                        choices=[
                            (b"", "Auto"),
                            (b"book", "Book"),
                            (b"slide", "Slide"),
                            (b"scroll", "Scroll"),
                        ],
                    ),
                ),
                (
                    "size",
                    models.CharField(
                        default=b"medium",
                        max_length=6,
                        verbose_name="Size",
                        choices=[
                            (b"small", "Small"),
                            (b"medium", "Medium"),
                            (b"big", "Big"),
                            (b"full", "Full"),
                        ],
                    ),
                ),
                (
                    "default_page",
                    models.IntegerField(
                        default=1,
                        help_text="Enter the page number to display by default",
                        verbose_name="Default page",
                    ),
                ),
                (
                    "actions",
                    models.CharField(
                        default=b"embed",
                        max_length=6,
                        verbose_name="Actions",
                        choices=[
                            (b"embed", "Open publication in full screen directly"),
                            (b"public", "Open description page"),
                            (b"view", "Open viewer directly"),
                        ],
                    ),
                ),
                (
                    "must_open_in_new_window",
                    models.BooleanField(
                        default=True, verbose_name="Open in new window"
                    ),
                ),
                (
                    "must_show_share_menu",
                    models.BooleanField(
                        default=True, verbose_name="Show the sharing menu after reading"
                    ),
                ),
                (
                    "must_show_book_title",
                    models.BooleanField(
                        default=True, verbose_name="Display the publication title"
                    ),
                ),
                (
                    "must_auto_flip",
                    models.BooleanField(
                        default=False, verbose_name="Automatically turn pages"
                    ),
                ),
            ],
            options={
                "verbose_name": "Publication",
                "verbose_name_plural": "Publications",
            },
            bases=("cms.cmsplugin",),
        ),
    ]
