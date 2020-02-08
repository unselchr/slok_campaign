from django.conf import settings
from django.db import models
from django.db.models import Q
from django.utils.translation import gettext as _

import apps.map.models as map_models


class Player(models.Model):

    game = models.ForeignKey('game.Game', verbose_name=_('Game'), related_name='players', on_delete=models.CASCADE)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('User'), related_name='players', on_delete=models.CASCADE)

    faction = models.CharField(_('Faction'), max_length=20)

    resource_points = models.SmallIntegerField(_('Resource Points'))

    victory_points = models.SmallIntegerField(_('Victory Points'))

    resource_dice_modifier = models.SmallIntegerField(_('Resource Dice Modifier'))

    def industry_total(self):
        return map_models.Territory.objects.filter(Q(planet__game=self.game), Q(player=self)).count()

    def resource_total(self):
        providence = 2
        modifier = self.resource_dice_modifier
        industry = self.industry_total()
        return providence + modifier + industry

    class Meta:
        unique_together = (
            ('game', 'user')
        )

    def __str__(self):
        return self.user.username
