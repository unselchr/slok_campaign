from django.db import models
from django.utils.translation import gettext as _


class Game(models.Model):

    name = models.CharField(_('Name'), max_length=30)

    # players = models.ManyToManyField('player.Player', related_name="" verbose_name=_('Users'))

    def __str__(self):
        return self.name


    class meta:
        unique = (
            'name'
        )
