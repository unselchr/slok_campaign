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


@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):

    search_fields = [
        'roster__player__user__username',
        'name',
        'datasheet',
        'battle_honors',
        'description',
        'wargear',
    ]

    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {}
