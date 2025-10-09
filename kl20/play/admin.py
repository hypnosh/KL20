
from django.contrib import admin
from .models import Level, Attempt, Player

@admin.register(Level)
class LevelAdmin(admin.ModelAdmin):
	list_display = ('level_identifier', 'name', 'checkpoint', 'question', 'answer', 'slug', 'prev_level')
	search_fields = ('name', 'question')

@admin.register(Attempt)
class AttemptAdmin(admin.ModelAdmin):
	list_display = ('timestamp', 'level', 'answer', 'correct', 'player')
	list_filter = ('correct', 'level', 'player')

@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
	list_display = ('name', 'email', 'is_admin')
	search_fields = ('name', 'email')
