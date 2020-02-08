from django.contrib import admin
from apps.map.models import Territory, Planet, Relic


class TerritoryInline(admin.TabularInline):
    model = Territory


@admin.register(Planet)
class PlanetAdmin(admin.ModelAdmin):
    inlines = [
        TerritoryInline,
    ]


@admin.register(Relic)
class RelicAdmin(admin.ModelAdmin):
    pass
