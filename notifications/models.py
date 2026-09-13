from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Notification(models.Model):
    """
    Модель уведомления пользователя.
    """
    
    NOTIFICATION_TYPES = [
        ('new_quote', 'Новая цитата'),
        ('new_comment', 'Новый комментарий'),
        ('like', 'Лайк'),
        ('friend_request', 'Запрос в друзья'),
        ('friend_accepted', 'Запрос принят'),
    ]
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='notifications',
        verbose_name='Получатель'
    )
    
    notification_type = models.CharField(
        max_length=20,
        choices=NOTIFICATION_TYPES,
        verbose_name='Тип уведомления'
    )
    
    message = models.TextField(
        verbose_name='Текст уведомления'
    )
    
    link = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='Ссылка'
    )
    
    is_read = models.BooleanField(
        default=False,
        verbose_name='Прочитано'
    )
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    
    class Meta:
        verbose_name = 'Уведомление'
        verbose_name_plural = 'Уведомления'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username}: {self.message[:50]}..."
    
    def mark_as_read(self):
        """Отмечает уведомление как прочитанное"""
        self.is_read = True
        self.save(update_fields=['is_read'])