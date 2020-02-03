from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views import generic

from apps.roster.models import Roster


class RosterListView(LoginRequiredMixin, generic.ListView):
    template_name = 'roster/roster_list.html'

    def get_queryset(self):
        return Roster.objects.filter(user = self.request.user)
