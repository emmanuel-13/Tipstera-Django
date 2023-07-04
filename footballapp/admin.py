from django.contrib import admin

from .models import Area, Competition, Team, Match


@admin.register(Area)
class AreaAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'flag']
    search_fields = ['name']


@admin.register(Competition)
class CompetitionAdmin(admin.ModelAdmin):
    list_display = ['area', 'name', 'code', 'emblem']
    search_fields = ['name']


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ['area', 'name', 'shortName', 'tla', 'crest']
    search_fields = ['id', 'name']


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ['competition', 'homeTeam', 'awayTeam', 'scoreHome', 'scoreAway', 'utcDate', 'status']
    search_fields = ['homeTeam', 'awayTeam']
