from django.db import models
from ckeditor.fields import RichTextField
from django.utils.translation import gettext_lazy as _


class Page(models.Model):

    key = models.CharField(
        verbose_name=_('Key'),
        unique=True,
        max_length=255,
    )

    content = RichTextField()

    created_at = models.DateTimeField(
        verbose_name=_('Created at'),
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        verbose_name=_('Updated at'),
        auto_now=True,
    )

    def __str__(self):
        return self.key
