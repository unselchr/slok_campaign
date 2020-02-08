from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q
from django.utils.translation import gettext as _


class Unit(models.Model):

    name = models.CharField(_('Name'), max_length=30)

    datasheet = models.CharField(_('Datasheet'), max_length=20)

    wargear = models.CharField(_('Wargear'), max_length=50, blank=True)

    experiance = models.SmallIntegerField(_('Experiance'))

    battle_honors = models.CharField(_('Battle Honors'), max_length=50, blank=True)

    description = models.CharField(_('Description'), max_length=50, blank=True)

    roster = models.ForeignKey('roster.roster', verbose_name=_('Roster'), on_delete=models.CASCADE, related_name='units')

    warlord = models.BooleanField(_('Warlord'))

    dead = models.BooleanField(_('dead'))

    cost = models.SmallIntegerField(_('Cost'))

    def clean(self):
        if self.warlord:
            try:
                temp = Unit.objects.get(Q(warlord=True), Q(roster=self.roster))
                if self == temp:
                    pass
                else:
                    raise ValidationError(_('You can only have on warlord.'))
            except Unit.DoesNotExist:
                pass

    def save(self, *args, **kwargs):
        if self.warlord and self.dead:
            self.warlord = False
        super(Unit, self).save(*args, **kwargs)


    class Meta:
        unique_together = (
            ('name', 'roster'),
            # ('roster', 'warlord'),
        )

    def __str__(self):
        return self.name


class KillTeam(models.Model):

    roster = models.OneToOneField('roster.roster', verbose_name=_('Roster'), on_delete=models.CASCADE, related_name='killTeam')

    def model_cost(self):
        return self.Models.objects.aggregate(Sum('cost'))

    def __str__(self):
        return str(self.roster)

class KillTeamModel(models.Model):

    killteam = models.ForeignKey('roster.killteam', verbose_name=_('Kill Team Model'), on_delete=models.CASCADE, related_name='killTeamModels')

    name = models.CharField(_('Name'), max_length=30)

    datasheet = models.CharField(_('DataSheet'), max_length=20)

    wargear = models.CharField(_('Wargear'), max_length=50, blank=True)

    experiance = models.SmallIntegerField(_('Experiance'))

    specialism = models.CharField(_('Specialism'), max_length=50, blank=True)

    demeanor = models.CharField(_('Demeanor'), max_length=50, blank=True)

    dead = models.BooleanField(_('dead'))

    cost = models.SmallIntegerField(_('Cost'))


    class meta:
        unique_together = (
            ('killteam', 'specialism')
        )

    def __str__(self):
        return self.name


class Roster(models.Model):

    player = models.OneToOneField('player.Player', verbose_name=_('Player'), on_delete=models.CASCADE, )

    def get_warlord(self):
        return self.units.get(warlord=True)

    def unit_cost(self):
        return self.units.aggregate(Sum('cost'))

    def __str__(self):
        return '%s %s' % (self.player, self.player.game)
