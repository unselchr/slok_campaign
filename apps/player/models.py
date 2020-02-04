from django.conf import settings
from django.db import models
from django.utils.translation import gettext as _


class Player(models.Model):

    game = models.ForeignKey('game.Game', verbose_name=_('Players'), on_delete=models.CASCADE)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('User'), on_delete=models.CASCADE)

    resource_points = models.SmallIntegerField(_('Resource Points'))

    victory_points = models.SmallIntegerField(_('Victory Points'))

    resource_dice_modifier = models.SmallIntegerField(_('Resource Dice Modifier'))
