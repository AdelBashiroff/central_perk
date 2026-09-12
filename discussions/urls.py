from django.urls import path
from . import views

app_name = 'discussions'

urlpatterns = [
    # Темы
    path('', views.thread_list, name='list'),
    path('<int:pk>/', views.thread_detail, name='detail'),
    path('create/', views.thread_create, name='create'),
    path('<int:pk>/edit/', views.thread_edit, name='edit'),
    path('<int:pk>/delete/', views.thread_delete, name='delete'),
    
    # Комментарии
    path('comment/<int:pk>/delete/', views.comment_delete, name='comment_delete'),
]