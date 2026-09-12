from django.urls import path

from . import views

app_name = 'api'

urlpatterns = [
    path('quotes/', views.QuoteListAPIView.as_view(), name='quote-list'),
    path('quotes/<int:pk>/', views.QuoteDetailAPIView.as_view(), name='quote-detail'),
    path('characters/', views.CharacterListAPIView.as_view(), name='character-list'),
    path('users/me/', views.CurrentUserAPIView.as_view(), name='user-me'),
]