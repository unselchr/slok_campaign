from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q
from apps.game import models as GameModels
from apps.player import models as PlayerModels
from apps.roster import models as RosterModels
from django.utils.translation import gettext as _


class Relic(models.Model):

    game = models.ForeignKey("game.Game", verbose_name=_("Game"), related_name='relics', on_delete=models.CASCADE)

    name = models.CharField(_('Name'), max_length=30)

    player = models.ForeignKey('player.Player', verbose_name=_('Player'), related_name='relics', on_delete=models.CASCADE, blank=True, null=True)

    holder = models.OneToOneField('roster.Unit', verbose_name='Holder', related_name='relic', on_delete=models.CASCADE, blank=True, null=True)

    description = models.CharField(_('Description'), max_length=50, blank=True)

    def clean(self):
        if self.player:
            if not self.holder:
                raise ValidationError(_('If there is a player there must be a holder'))
            try:
                GameModels.Game.objects.get(players=self.player)
            except GameModels.Game.DoesNotExist:
                raise ValidationError(_('Player must be in selected game'))
            if self.holder:
                try:
                    PlayerModels.Player.objects.get(roster__units=self.holder)
                except PlayerModels.Player.DoesNotExist:
                    raise ValidationError(_('Holder must be a member of the chosen players roster'))
            else:
                raise ValidationError(_('If there is a holder there must be a player'))


    class Meta:
        unique_together = (
            ('game', 'name'),
        )

    def __str__(self):
        return self.name


class Planet(models.Model):

    game = models.ForeignKey("game.Game", verbose_name=_("Game"), related_name='planets', on_delete=models.CASCADE)

    name = models.CharField(_('Name'), max_length=30)


    class Meta:
        unique_together = (
            ('game', 'name')
        )

    def __str__(self):
        return self.name


class Territory(models.Model):

    name = models.CharField(_('name'), max_length=30)

    description = models.CharField(_("Description"), max_length=75, blank=True, null=True)

    planet = models.ForeignKey('map.Planet', verbose_name=_('Planet'), related_name='territories', on_delete=models.CASCADE)

    INDUSTRY, FORTIFICATION, CRITICAL_LOCATION = 'industry', 'fortification', 'critical_location'
    FEATURE_CHOICES = (
        (INDUSTRY, _('Industry')),
        (FORTIFICATION, _('Fortification')),
        (CRITICAL_LOCATION, _('Critical Location')),
    )

    feature = models.CharField(_('feature'), max_length=30, choices=FEATURE_CHOICES, blank=True, null=True)

    player = models.ForeignKey(
        'player.Player',
        verbose_name=_('Player'),
        related_name='territories',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )

    def clean(self):
        if self.player:
            try:
                GameModels.Game.objects.get(Q(planets=self.planet), Q(players=self.player))
            except GameModels.Game.DoesNotExist:
                raise ValidationError(_('Player must be a member of the game this territory is in.'))


    class Meta:
        unique_together = (
            ('name', 'planet')
        )

    def __str__(self):
        return self.name
