from django.db import models


class Character(models.Model):
    """
    Модель персонажа из сериала
    Хранит информацию о нем
    """
    
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='Имя персонажа'
    )
    
    actor_name = models.CharField(
        max_length=100,
        verbose_name='Имя актера'
    )
    
    photo = models.ImageField(
        upload_to='characters/',
        null=True,
        blank=True,
        verbose_name='Фото'
    )
    
    description = models.TextField(
        blank=True,
        verbose_name='Описание'
    )
    
    fun_fact = models.TextField(
        blank=True,
        verbose_name='Интересный факт'
    )
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    
    class Meta:
        verbose_name = 'Персонаж'
        verbose_name_plural = 'Персонажи'
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} ({self.actor_name})"
    
    def get_quotes(self):
        """Возвращает цитаты этого персонажа"""
        return self.quotes.all()
    
