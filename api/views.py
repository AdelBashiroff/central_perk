from rest_framework import generics, permissions
from drf_spectacular.utils import extend_schema

from quotes.models import Quote
from characters.models import Character
from django.contrib.auth import get_user_model

from .serializers import QuoteSerializer, CharacterSerializer, UserSerializer

User = get_user_model()


@extend_schema(
    summary="Список цитат",
    description="Возвращает список всех цитат с фильтрацией по персонажу и поиском по тексту.",
)
class QuoteListAPIView(generics.ListAPIView):
    """
    API для получения списка цитат.
    """
    serializer_class = QuoteSerializer

    def get_queryset(self):
        """Фильтрация цитат по параметрам запроса"""
        queryset = Quote.objects.all().order_by('-created_at')

        character = self.request.query_params.get('character')
        if character:
            queryset = queryset.filter(character__name__icontains=character)

        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(text__icontains=search)

        return queryset


@extend_schema(
    summary="Детальная информация о цитате",
    description="Возвращает полную информацию о конкретной цитате по её ID.",
)
class QuoteDetailAPIView(generics.RetrieveAPIView):
    """
    API для получения детальной информации о цитате.
    """
    queryset = Quote.objects.all()
    serializer_class = QuoteSerializer


@extend_schema(
    summary="Список персонажей",
    description="Возвращает список всех персонажей сериала 'Друзья'.",
)
class CharacterListAPIView(generics.ListAPIView):
    """
    API для получения списка персонажей.
    """
    queryset = Character.objects.all()
    serializer_class = CharacterSerializer


@extend_schema(
    summary="Информация о текущем пользователе",
    description="Возвращает информацию о текущем авторизованном пользователе.",
)
class CurrentUserAPIView(generics.RetrieveAPIView):
    """
    API для получения информации о текущем пользователе.
    GET /api/users/me/
    """
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """Возвращает текущего пользователя"""
        return self.request.user