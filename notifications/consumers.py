import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async


class NotificationConsumer(AsyncWebsocketConsumer):
    """
    WebSocket Consumer для отправки живых уведомлений.
    """
    
    async def connect(self):
        """Подключение пользователя"""
        self.user = self.scope['user']
        
        # Проверяем авторизацию
        if not self.user.is_authenticated:
            await self.close()
            return
        
        # Группа для этого пользователя
        self.group_name = f'notifications_{self.user.id}'
        
        # Добавляем в группу
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        
        await self.accept()
        
        # Отправляем непрочитанные
        await self.send_unread_notifications()
    
    async def disconnect(self, close_code):
        """Отключение пользователя"""
        if hasattr(self, 'group_name'):
            await self.channel_layer.group_discard(
                self.group_name,
                self.channel_name
            )
    
    async def receive(self, text_data):
        """Получение данных от клиента"""
        data = json.loads(text_data)
        
        if data.get('type') == 'mark_read':
            await self.mark_notification_read(data.get('id'))
    
    async def send_notification(self, event):
        """Отправка уведомления клиенту"""
        await self.send(text_data=json.dumps({
            'type': 'notification',
            'id': event['id'],
            'message': event['message'],
            'link': event['link'],
            'notification_type': event['notification_type'],
            'created_at': event['created_at'],
        }))
    
    @database_sync_to_async
    def send_unread_notifications(self):
        """Отправляет непрочитанные уведомления"""
        from .models import Notification
        
        notifications = Notification.objects.filter(
            user=self.user,
            is_read=False
        )[:10]
        
        for notification in notifications:
            self.send(text_data=json.dumps({
                'type': 'notification',
                'id': notification.id,
                'message': notification.message,
                'link': notification.link,
                'notification_type': notification.notification_type,
                'created_at': str(notification.created_at),
            }))
    
    @database_sync_to_async
    def mark_notification_read(self, notification_id):
        """Отмечает уведомление как прочитанное"""
        from .models import Notification
        
        try:
            notification = Notification.objects.get(
                id=notification_id,
                user=self.user
            )
            notification.mark_as_read()
        except Notification.DoesNotExist:
            pass