from django.contrib import admin
from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """
    Админка для отзывов.
    """
    list_display = ('id', 'user', 'episode', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('user__username', 'episode__title', 'text')
    readonly_fields = ('created_at', 'updated_at')
    raw_id_fields = ('user', 'episode')