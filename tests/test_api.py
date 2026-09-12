import pytest
from django.urls import reverse
from rest_framework import status
from quotes.models import Quote


# ============================================================
# Тесты API: QuoteListAPIView
# ============================================================

@pytest.mark.django_db
class TestQuoteListAPI:
    """Тесты для API списка цитат"""
    
    def test_list_quotes_unauthorized(self, api_client, quote):
        """Тест: неавторизованный пользователь может читать"""
        url = reverse('api:quote-list')
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1
        assert response.data['results'][0]['text'] == quote.text
    
    def test_list_quotes_authorized(self, authenticated_client, quote):
        """Тест: авторизованный пользователь видит цитаты"""
        url = reverse('api:quote-list')
        response = authenticated_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 1
    
    def test_list_quotes_empty(self, api_client):
        """Тест: пустой список цитат"""
        url = reverse('api:quote-list')
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 0
        assert response.data['results'] == []
    
    def test_filter_by_character(self, api_client, user, character):
        """Тест: фильтрация по персонажу"""
        # Создаем 2 цитаты
        Quote.objects.create(
            text='Could I BE any more...?',
            character=character,
            author=user
        )
        
        from characters.models import Character
        joey = Character.objects.create(
            name='Joey Tribbiani',
            actor_name='Matt LeBlanc'
        )
        Quote.objects.create(
            text='How you doin?',
            character=joey,
            author=user
        )
        
        # Фильтруем по Chandler
        url = reverse('api:quote-list')
        response = api_client.get(url, {'character': 'Chandler'})
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 1
        assert 'Chandler' in response.data['results'][0]['character_name']
    
    def test_search_by_text(self, api_client, user, character):
        """Тест: поиск по тексту"""
        Quote.objects.create(
            text='Could I BE any more...?',
            character=character,
            author=user
        )
        Quote.objects.create(
            text='How you doin?',
            character=character,
            author=user
        )
        
        url = reverse('api:quote-list')
        response = api_client.get(url, {'search': 'How you doin'})
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 1
        assert 'How you doin' in response.data['results'][0]['text']
    
    def test_quote_detail(self, api_client, quote):
        """Тест: детальная информация о цитате"""
        url = reverse('api:quote-detail', kwargs={'pk': quote.pk})
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] == quote.pk
        assert response.data['text'] == quote.text
    
    def test_quote_detail_not_found(self, api_client):
        """Тест: цитата не найдена"""
        url = reverse('api:quote-detail', kwargs={'pk': 9999})
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_404_NOT_FOUND


# ============================================================
# Тесты API: CharacterListAPIView
# ============================================================

@pytest.mark.django_db
class TestCharacterListAPI:
    """Тесты для API списка персонажей"""
    
    def test_list_characters(self, api_client, character):
        """Тест: список персонажей"""
        url = reverse('api:character-list')
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 1
        assert response.data['results'][0]['name'] == character.name


# ============================================================
# Тесты API: CurrentUserAPIView
# ============================================================

@pytest.mark.django_db
class TestCurrentUserAPI:
    """Тесты для API текущего пользователя"""
    
    def test_current_user_unauthorized(self, api_client):
        """Тест: неавторизованный пользователь — 403"""
        url = reverse('api:user-me')
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_current_user_authorized(self, authenticated_client, user):
        """Тест: авторизованный пользователь видит себя"""
        url = reverse('api:user-me')
        response = authenticated_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['username'] == user.username
        assert response.data['email'] == user.email