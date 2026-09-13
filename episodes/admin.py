from django.contrib import admin
from .models import Episode


@admin.register(Episode)
class EpisodeAdmin(admin.ModelAdmin):
    """
    Админка для серий.
    """
    list_display = ('id', 'title', 'season', 'episode_number', 'air_date', 'rating_average')
    list_filter = ('season',)
    search_fields = ('title', 'description')
    ordering = ('season', 'episode_number')
    readonly_fields = ('created_at', 'updated_at')
    
    def rating_average(self, obj):
        """Средний рейтинг серии"""
        return obj.get_rating_average()
    rating_average.short_description = 'Рейтинг'