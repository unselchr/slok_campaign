from django.contrib import admin
from apps.roster.models import KillTeam, KillTeamModel, Roster, Unit

admin.site.register(KillTeam)
admin.site.register(KillTeamModel)
admin.site.register(Roster)
admin.site.register(Unit)