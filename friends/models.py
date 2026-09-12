from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class FriendshipRequest(models.Model):
    """
    Модель запроса в друзья.
    Управляет отношениями между пользователями.
    """
    
    STATUS_CHOICES = [
        ('pending', 'Ожидает'),
        ('accepted', 'Принят'),
        ('rejected', 'Отклонен'),
    ]
    
    from_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sent_friend_requests',
        verbose_name='От кого'
    )
    
    to_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='received_friend_requests',
        verbose_name='Кому'
    )
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name='Статус'
    )
    
    message = models.TextField(
        blank=True,
        verbose_name='Сообщение'
    )
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    
    class Meta:
        verbose_name = 'Запрос в друзья'
        verbose_name_plural = 'Запросы в друзья'
        ordering = ['-created_at']
        unique_together = ['from_user', 'to_user']  # Уникальность пары
    
    def __str__(self):
        return f"{self.from_user.username} -> {self.to_user.username} ({self.status})"
    
    def accept(self):
        """Принять запрос в друзья"""
        self.status = 'accepted'
        self.save()
        # Добавляем друг друга в друзья
        self.from_user.friends.add(self.to_user)
        self.to_user.friends.add(self.from_user)
    
    def reject(self):
        """Отклонить запрос в друзья"""
        self.status = 'rejected'
        self.save()