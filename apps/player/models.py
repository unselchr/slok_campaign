from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q
from django.utils.translation import gettext as _

import apps.map.models as map_models


class Player(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('User'), related_name='players', on_delete=models.CASCADE)
    game = models.ForeignKey('game.Game', verbose_name=_('Game'), related_name=_('players'), on_delete=models.CASCADE)

    faction = models.CharField(_('Faction'), max_length=20)

    resource_points = models.SmallIntegerField(_('Resource Points'))

    RAID_SUPPLY_LINES, FORWARD_CONSTRUCTION, WARP_STORM, ISSUE_SPECIAL_ORDERS, RECONNAISSANCE = 'raid', 'construction', 'storm', 'orders', 'recon'
    AGGRESSIVE_DIPLOMACY, PRIORITIZE_COLONIZATION, ENLIST_SPECIAL_FORCES, DRILL_SOLDIERS, TRAIN_LEADERS = 'diplomacy', 'colonization', 'special_forces', 'drill', 'train'

    EVENT_CHOICES = (
        (RAID_SUPPLY_LINES, 'Raid Supply Lines'),
        (FORWARD_CONSTRUCTION, 'Forward Construction'),
        (WARP_STORM, 'Warp Storm'),
        (ISSUE_SPECIAL_ORDERS, 'Issue Special Orders'),
        (RECONNAISSANCE, 'Reconnaissandce'),
        (AGGRESSIVE_DIPLOMACY, 'Aggressive Diplomacy'),
        (PRIORITIZE_COLONIZATION, 'Prioritize Colonization'),
        (ENLIST_SPECIAL_FORCES, 'Enlist Special Forces'),
        (DRILL_SOLDIERS, 'Drill the Soldiers'),
        (TRAIN_LEADERS, 'Train the Leaders'),
    )

    EVENT_REQUIRE_TARGET = (RAID_SUPPLY_LINES, WARP_STORM, RECONNAISSANCE)

    event = models.CharField(_('Event'), max_length=15, choices=EVENT_CHOICES, unique=True, blank=True, null=True)

    event_target = models.ForeignKey('player.Player', verbose_name=_('Event Target'), related_name='event_targeter', on_delete=models.CASCADE, blank=True, null=True)

    opponent = models.ForeignKey('player.Player', verbose_name=_('Opponent'), related_name='challenger', on_delete=models.CASCADE, blank=True, null=True)

    challenge_location = models.OneToOneField('map.Territory', verbose_name=_('Challenge Location'), related_name='challenger', on_delete=models.CASCADE, blank=True, null=True)

    subterfuge_target = models.ForeignKey('player.Player', verbose_name=_('Subterfuge Target'), related_name='subterfuge_targeter', on_delete=models.CASCADE, blank=True, null=True)

    reconnaissance_subterfuge_target = models.ForeignKey('player.Player', verbose_name=_('Extra Subterfuge Target'), related_name='reconnaissance_subterfuge_targeter', on_delete=models.CASCADE, blank=True, null=True)

    SABOTAGE_FORTIFICATIONS, RESCUE_PRISONERS, SEIZE_GROUND, DISRUPT_SUPPLIES, AMBUSH = 'sabatoge', 'rescue', 'seize', 'disrupt', 'ambush'
    FEINT, ASSASSINATE, TAKE_PRISONERS, ROOT_OUT, SEEK_INTELLIGENCE, TERROR_TACTICS = 'feint', 'assassinate', 'take_prisoners', 'root_out', 'intelligence', 'terror'

    SUBTERFUGE_CHOICES = (
        (SABOTAGE_FORTIFICATIONS, 'Sabatoge Fortifications'),
        (RESCUE_PRISONERS, 'Rescue Prisoners'),
        (SEIZE_GROUND, 'Seize Ground'),
        (DISRUPT_SUPPLIES, 'Disrupt Supplies'),
        (AMBUSH, 'Ambush'),
        (FEINT, 'Feint'),
        (ASSASSINATE, 'Assassinate'),
        (TAKE_PRISONERS, 'Take Prisoners'),
        (ROOT_OUT, 'Root Out Enemy Agents'),
        (SEEK_INTELLIGENCE, 'Seek Intelligence'),
        (TERROR_TACTICS, 'Terror Tactics'),
    )

    subterfuge_mission = models.CharField(_('Subterfuge Mission'), max_length=20, choices=SUBTERFUGE_CHOICES, blank=True, null=True)

    reconnaissance_subterfuge_mission = models.CharField(_('Extra Subterfuge Mission'), max_length=20, choices=SUBTERFUGE_CHOICES, blank=True, null=True)

    campaign_points = models.IntegerField(_('Campaign Points'))

    def victory_points(self):
        provinces = map_models.Territory.objects.filter(Q(planet__game=self.game), Q(player=self)).count()
        critical_locations = map_models.Territory.objects.filter(
            Q(planet__game=self.game),
            Q(player=self),
            Q(feature=map_models.Territory.CRITICAL_LOCATION)
        ).count()
        relics = map_models.Relic.objects.filter(player=self).count()
        return provinces + critical_locations + relics

    resource_dice_modifier = models.SmallIntegerField(_('Resource Dice Modifier'))

    def industry_total(self):
        return map_models.Territory.objects.filter(
            Q(planet__game=self.game),
            Q(player=self),
            Q(feature=map_models.Territory.INDUSTRY)
        ).count()

    def resource_total(self):
        providence = 2
        modifier = self.resource_dice_modifier
        industry = self.industry_total()
        return providence + modifier + industry

    def clean(self):
        if self.game.players >=10:
            raise ValidationError(_('Max of 10 players per game.'))

        if any((self.subterfuge_mission, self.subterfuge_target)) and not all(self.subterfuge_mission, self.subterfuge_target):
            raise ValidationError(_('Subterfuge missions need a target and targets need a mission'))

        if self.event in EVENT_REQUIRE_TARGET and not self.event_target:
            raise ValidationError(_('This event requires a target'))
        elif self.event not in EVENT_REQUIRE_TARGET and self.event_target:
            raise ValidationError(_('This event does not require a target'))

        if self.event != RECONNAISANCE and (self.reconnaissance_subterfuge_mission or self.reconnaissance_subterfuge_target):
            raise ValidationError(_('You cannot have an extra subterfuge mission or target unless you chose Reconnaisance as an event'))
        elif any((self.reconnaissance_subterfuge_mission, self.reconnaissance_subterfuge_target)) and not all((self.reconnaissance_subterfuge_mission, self.reconnaissance_subterfuge_target)):
            raise ValidationError(_('Subterfuge missions need a target and targets need a mission'))

        if self.challenger and self.opponent:
            raise ValidationError(_('You cannot challenge someone if you have already been challenged'))


    class Meta:
        unique_together = (
            ('game', 'user'),
            ('event', 'event_target'),
            ('subterfuge_mission', 'subterfuge_target'),
            ('reconnaissance_subterfuge_mission', 'reconnaissance_subterfuge_target'),
            ('subterfuge_mission','reconnaissance_subterfuge_mission', 'subterfuge_target'),
            ('subterfuge_mission','reconnaissance_subterfuge_mission', 'reconnaissance_subterfuge_target'),
        )

    def __str__(self):
        return self.user.username
