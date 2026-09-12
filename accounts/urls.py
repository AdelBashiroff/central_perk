from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'

urlpatterns = [
    # Регистрация
    path('register/', views.register, name='register'),
    
    # Вход и выход
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    # Профиль
    path('profile/', views.profile_view, name='profile'),
    
    # Смена пароля
    path('password-change/', views.CustomPasswordChangeView.as_view(), name='password_change'),
    
    # Восстановление пароля (через allauth)
    # Будет обрабатываться через allauth.urls
]