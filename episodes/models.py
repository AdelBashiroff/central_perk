from django.db import models
from characters.models import Character


class Episode(models.Model):
    """
    Модель серии сериала
    Хранит информацию о каждой серии
    """
    
    title = models.CharField(
        max_length=200,
        verbose_name='Название серии'
    )
    
    season = models.PositiveIntegerField(
        verbose_name='Сезон'
    )
    
    episode_number = models.PositiveIntegerField(
        verbose_name='Номер серии'
    )
    
    description = models.TextField(
        blank=True,
        verbose_name='Описание'
    )
    
    air_date = models.DateField(
        null=True,
        blank=True,
        verbose_name='Дата выхода'
    )
    
    screenshot = models.ImageField(
        upload_to='episodes/screenshots/',
        null=True,
        blank=True,
        verbose_name='Скриншот'
    )
    
    video_file = models.FileField(
        upload_to='episodes/videos/',
        null=True,
        blank=True,
        verbose_name='Видео файл'
    )
    
    # Связь с персонажами (многие-ко-многим)
    characters = models.ManyToManyField(
        Character,
        related_name='episodes',
        blank=True,
        verbose_name='Персонажи в серии'
    )
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    
    class Meta:
        verbose_name = 'Серия'
        verbose_name_plural = 'Серии'
        ordering = ['season', 'episode_number']
    
    def __str__(self):
        return f"S{self.season:02d}E{self.episode_number:02d} - {self.title}"
    
    def get_rating_average(self):
        """Возвращает средний рейтинг серии"""
        reviews = self.reviews.all()
        if reviews.exists():
            total = sum(review.rating for review in reviews)
            return round(total / reviews.count(), 1)
        return 0