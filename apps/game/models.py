from django.conf import settings
from django.db import models
from django.utils.translation import gettext as _


class Game(models.Model):

    name = models.CharField(_("Name"), max_length=30)

    users = models.ManyToManyField(settings.AUTH_USER_MODEL, verbose_name=_("Users"))

    def __str__(self):
        return self.name