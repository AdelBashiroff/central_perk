from django.contrib import admin
from .models import DiscussionThread, Comment


@admin.register(DiscussionThread)
class DiscussionThreadAdmin(admin.ModelAdmin):
    """
    Админка для тем обсуждений.
    """
    list_display = ('id', 'title', 'user', 'views', 'comments_count', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('title', 'content', 'user__username')
    readonly_fields = ('views', 'created_at', 'updated_at')
    raw_id_fields = ('user', 'episode')
    
    def comments_count(self, obj):
        """Количество комментариев"""
        return obj.get_comments_count()
    comments_count.short_description = 'Комментариев'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """
    Админка для комментариев.
    """
    list_display = ('id', 'user', 'thread', 'content_preview', 'parent', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('content', 'user__username', 'thread__title')
    readonly_fields = ('created_at', 'updated_at')
    raw_id_fields = ('user', 'thread', 'parent')
    
    def content_preview(self, obj):
        """Превью комментария"""
        return obj.content[:50] + "..." if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Комментарий'