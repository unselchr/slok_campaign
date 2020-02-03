from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views import generic

from apps.game.models import Game

def user_is_member(user, game):
    return user and user in game.users


class GameListView(LoginRequiredMixin, generic.ListView):

    template_name = 'game/game_list.html'

    def get_queryset(self):
        games = Game.objects.filter(users=self.request.user)
        print(games)
        return games
