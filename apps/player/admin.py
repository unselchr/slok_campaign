from django.contrib import admin
from apps.player.models import Player


@admin.register(Player)
class PlayerModelAdmin(admin.ModelAdmin):
    pass
