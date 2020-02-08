from django.contrib import admin
from apps.roster.models import KillTeam, KillTeamModel, Roster, Unit


class KillTeamModelInline(admin.TabularInline):
    model = KillTeamModel


@admin.register(KillTeam)
class KillTeamAdmin(admin.ModelAdmin):
    inlines = [
        KillTeamModelInline
    ]


class UnitInline(admin.TabularInline):
    model = Unit


@admin.register(Roster)
class RosterAdmin(admin.ModelAdmin):
    inlines = [
        UnitInline,
    ]
