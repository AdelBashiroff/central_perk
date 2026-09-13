from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Notification


def send_notification(user, notification_type, message, link=''):
    """
    Создает уведомление и отправляет через WebSocket.
    """
    # Создаем в БД
    notification = Notification.objects.create(
        user=user,
        notification_type=notification_type,
        message=message,
        link=link
    )
    
    # Отправляем через WebSocket
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f'notifications_{user.id}',
        {
            'type': 'send_notification',
            'id': notification.id,
            'message': notification.message,
            'link': notification.link,
            'notification_type': notification.notification_type,
            'created_at': str(notification.created_at),
        }
    )
    
    return notification