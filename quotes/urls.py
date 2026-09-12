from django.urls import path
from . import views

app_name = 'quotes'

urlpatterns = [
    # READ - список
    path('', views.quote_list, name='list'),
    
    # READ - детально
    path('<int:pk>/', views.quote_detail, name='detail'),
    
    # CREATE
    path('create/', views.quote_create, name='create'),
    
    # UPDATE
    path('<int:pk>/edit/', views.quote_edit, name='edit'),
    
    # DELETE
    path('<int:pk>/delete/', views.quote_delete, name='delete'),
    
    # LIKE
    path('<int:pk>/like/', views.quote_like, name='like'),
]