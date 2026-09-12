import pytest
from quotes.models import Quote
from discussions.models import Comment


# ============================================================
# Тесты модели Quote
# ============================================================

@pytest.mark.django_db
class TestQuoteModel:
    """Тесты для модели Quote"""
    
    def test_create_quote(self, user, character):
        """Тест создания цитаты"""
        quote = Quote.objects.create(
            text='How you doin?',
            character=character,
            author=user
        )
        
        assert quote.text == 'How you doin?'
        assert quote.character == character
        assert quote.author == user
        assert quote.pk is not None
        assert str(quote) == f"{character.name}: How you doin?..."
    
    def test_quote_str(self, quote, character):
        """Тест метода __str__"""
        expected = f"{character.name}: {quote.text[:50]}..."
        assert str(quote) == expected
    
    def test_quote_likes_count(self, quote, another_user):
        """Тест подсчета лайков"""
        assert quote.get_likes_count() == 0
        
        quote.likes.add(another_user)
        assert quote.get_likes_count() == 1
    
    def test_quote_is_liked_by_user(self, quote, another_user):
        """Тест проверки лайка пользователем"""
        assert quote.is_liked_by_user(another_user) is False
        
        quote.likes.add(another_user)
        assert quote.is_liked_by_user(another_user) is True
    
        
     


# ============================================================
# Тесты модели Comment
# ============================================================

@pytest.mark.django_db
class TestCommentModel:
    """Тесты для модели Comment"""
    
    def test_create_comment(self, thread, user):
        """Тест создания комментария"""
        comment = Comment.objects.create(
            thread=thread,
            user=user,
            content='Отличная тема!'
        )
        
        assert comment.content == 'Отличная тема!'
        assert comment.thread == thread
        assert comment.user == user
        assert comment.parent is None
        assert comment.pk is not None
    
    def test_comment_str(self, comment, user):
        """Тест метода __str__"""
        expected = f"{user.username}: {comment.content[:50]}..."
        assert str(comment) == expected
    
    
    def test_comment_is_reply(self, thread, user, comment):
        """Тест: комментарий является ответом"""
        reply = Comment.objects.create(
            thread=thread,
            user=user,
            content='Согласен!',
            parent=comment
        )
        
        assert reply.is_reply() is True
        assert reply.parent == comment
    
    def test_comment_replies_count(self, thread, user, comment):
        """Тест подсчета ответов"""
        assert comment.get_replies_count() == 0
        
        Comment.objects.create(
            thread=thread,
            user=user,
            content='Ответ 1',
            parent=comment
        )
        Comment.objects.create(
            thread=thread,
            user=user,
            content='Ответ 2',
            parent=comment
        )
        
        assert comment.get_replies_count() == 2