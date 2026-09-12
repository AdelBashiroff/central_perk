from rest_framework import serializers
from django.contrib.auth import get_user_model

from quotes.models import Quote
from characters.models import Character

User = get_user_model()


class CharacterSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Character.
    """
    
    class Meta:
        model = Character
        fields = ['id', 'name', 'actor_name', 'photo', 'description']


class QuoteSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Quote.
    """
    
    character_name = serializers.CharField(source='character.name', read_only=True)
    author_username = serializers.CharField(source='author.username', read_only=True)
    likes_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    
    class Meta:
        model = Quote
        fields = [
            'id', 'text', 'character', 'character_name',
            'author_username', 'likes_count', 'is_liked',
            'created_at'
        ]
    
    def get_likes_count(self, obj):
        """Возвращает количество лайков"""
        return obj.get_likes_count()
    
    def get_is_liked(self, obj):
        """Проверяет, лайкнул ли текущий пользователь"""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.is_liked_by_user(request.user)
        return False


class UserSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели CustomUser.
    """
    
    quotes_count = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'avatar',
            'bio', 'favorite_character', 'quotes_count'
        ]
    
    def get_quotes_count(self, obj):
        """Возвращает количество цитат пользователя"""
        return obj.quotes.count()