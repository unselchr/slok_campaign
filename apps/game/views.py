from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.views import generic

from apps.game.models import Game

def user_is_member(user, game):
    return user and user in game.users


class GameListView(LoginRequiredMixin, generic.ListView):

    template_name = 'game/game_list.html'

    def get_queryset(self):
        games = Game.objects.filter(players__user=self.request.user)
        return games


class GameDetailView(LoginRequiredMixin, generic.DetailView):

    model = Game
    template_name = 'game/game_detail.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if request.user.players.filter(game=self.object):
            return super().get(request, *args, **kwargs)
        else:
            return redirect('home')
