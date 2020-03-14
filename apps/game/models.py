from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


class Game(models.Model):

    name = models.CharField(_('Name'), max_length=30, unique=True)

    game_master = models.ForeignKey('player.Player', related_name='master_of', verbose_name=_('Game Master'), on_delete=models.CASCADE, null=True)

    turn = models.PositiveIntegerField(_('Turn'), default=0)

    REVENUE, EVENT, CHALLENGE, SUBTERFUGE, SPOILS = 'revenue', 'event', 'challenge', 'subterfuge', 'spoils'

    PHASE_CHOICES = (
        (REVENUE, 'Revenue Phase'),
        (EVENT, 'Event Phase'),
        (CHALLENGE, 'Challenge Phase'),
        (SUBTERFUGE, 'Subterfuge Phase'),
        (SPOILS, 'Spoils Phase'),
    )

    phase = models.CharField(_('Phase'), choices=PHASE_CHOICES, max_length=50, default=REVENUE)

    def current_battles(self):
        battles = self.battles.filter(turn=self.turn)
        return battles

    def clean(self):
        if self.game_master and self.game_master not in self.players:
            raise ValidationError(_('Game master must be a member of the game!'))

    def __str__(self):
        return self.name


    # class Meta:
    #     unique = (
    #         'name'
    #     )


# class BattleParticipant(models.Model):


class Battle(models.Model):

    game = models.ForeignKey('game.Game', verbose_name=_('Game'), related_name='battles', on_delete=models.CASCADE)

    participants = models.ManyToManyField("player.Player", verbose_name=_("Participants"), related_name='battles')

    winner = models.ForeignKey('player.Player', verbose_name=_('Winner'), related_name='battles_won', on_delete=models.CASCADE)

    turn = models.PositiveIntegerField(_("Turn"), editable=False)

    irl_location = models.CharField(_("Real Life Location"), max_length=50)

    date = models.DateTimeField(_("Date"), auto_now=False, auto_now_add=False)

    location = models.ForeignKey("map.Territory", verbose_name=_("Location"), related_name="battles", on_delete=models.CASCADE)

    def __str__(self):
        return ' vs '.join(self.participants.all())
