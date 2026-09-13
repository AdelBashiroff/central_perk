from django.contrib import admin
from .models import FriendshipRequest


@admin.register(FriendshipRequest)
class FriendshipRequestAdmin(admin.ModelAdmin):
    """
    Админка для запросов в друзья.
    """
    list_display = ('id', 'from_user', 'to_user', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('from_user__username', 'to_user__username', 'message')
    readonly_fields = ('created_at', 'updated_at')
    raw_id_fields = ('from_user', 'to_user')
    
    actions = ['accept_requests', 'reject_requests']
    
    def accept_requests(self, request, queryset):
        """Принять выбранные запросы"""
        for friendship_request in queryset:
            friendship_request.accept()
        self.message_user(request, f'Принято: {queryset.count()}')
    accept_requests.short_description = 'Принять выбранные'
    
    def reject_requests(self, request, queryset):
        """Отклонить выбранные запросы"""
        for friendship_request in queryset:
            friendship_request.reject()
        self.message_user(request, f'Отклонено: {queryset.count()}')
    reject_requests.short_description = 'Отклонить выбранные'