import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from quotes.models import Quote
from characters.models import Character
from discussions.models import DiscussionThread, Comment

User = get_user_model()


@pytest.fixture
def user(db):
    """Создает тестового пользователя"""
    return User.objects.create_user(
        username='chandler',
        email='chandler@friends.com',
        password='secret123'
    )


@pytest.fixture
def another_user(db):
    """Создает второго пользователя"""
    return User.objects.create_user(
        username='joey',
        email='joey@friends.com',
        password='secret123'
    )


@pytest.fixture
def character(db):
    """Создает тестового персонажа"""
    return Character.objects.create(
        name='Chandler Bing',
        actor_name='Matthew Perry',
        description='Король сарказма'
    )


@pytest.fixture
def quote(db, user, character):
    """Создает тестовую цитату"""
    return Quote.objects.create(
        text='Could I BE any more...?',
        character=character,
        author=user
    )


@pytest.fixture
def thread(db, user):
    """Создает тестовую тему обсуждения"""
    return DiscussionThread.objects.create(
        title='Любимая цитата Чендлера',
        content='Какая ваша любимая цитата?',
        user=user
    )


@pytest.fixture
def comment(db, thread, user):
    """Создает тестовый комментарий"""
    return Comment.objects.create(
        thread=thread,
        user=user,
        content='Мне нравится "Could I BE any more...?"'
    )


@pytest.fixture
def api_client():
    """Создает API-клиент"""
    return APIClient()


@pytest.fixture
def authenticated_client(api_client, user):
    """Создает авторизованный API-клиент"""
    api_client.force_authenticate(user=user)
    return api_client