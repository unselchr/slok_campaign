from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


class Game(models.Model):

    name = models.CharField(_('Name'), max_length=30, unique=True)

    game_master = models.ForeignKey("player.Player", related_name="master_of", verbose_name=_("Game Master"), on_delete=models.CASCADE, null=True)

    def clean(self):
        if self.game_master and self.game_master not in self.players:
            raise ValidationError(_('Game master must be a member of the game!'))

    def __str__(self):
        return self.name


    # class Meta:
    #     unique = (
    #         'name'
    #     )
