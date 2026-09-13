from django.contrib import admin
from .models import Character


@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    """
    Админка для персонажей.
    """
    list_display = ('id', 'name', 'actor_name', 'created_at')
    search_fields = ('name', 'actor_name')
    readonly_fields = ('created_at', 'updated_at')
    
    def quotes_count(self, obj):
        """Количество цитат персонажа"""
        return obj.get_quotes_count()
    quotes_count.short_description = 'Цитат'