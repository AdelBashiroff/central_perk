from django.contrib import admin
from .models import Quote


@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    """
    Админка для цитат.
    """
    list_display = ('id', 'text_preview', 'character', 'episode', 'author', 'likes_count', 'created_at')
    list_filter = ('character', 'created_at')
    search_fields = ('text', 'character__name', 'author__username')
    readonly_fields = ('created_at', 'updated_at')
    raw_id_fields = ('character', 'episode', 'author')
    filter_horizontal = ('likes',)
    
    def text_preview(self, obj):
        """Превью текста цитаты"""
        return obj.text[:50] + "..." if len(obj.text) > 50 else obj.text
    text_preview.short_description = 'Текст'
    
    def likes_count(self, obj):
        """Количество лайков"""
        return obj.get_likes_count()
    likes_count.short_description = 'Лайков'