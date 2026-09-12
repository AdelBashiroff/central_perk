from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from .views import home

urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    
    # Все приложения с namespace
    path('quotes/', include('quotes.urls')),         # quotes:list, quotes:detail
    path('accounts/', include('accounts.urls')),     # accounts:login, accounts:register
    path('discussions/', include('discussions.urls')), # discussions:list
    path('accounts/', include('allauth.urls')),
    
    # API
    path('api/', include('api.urls')),
    
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    
    path('api/auth/', include('dj_rest_auth.urls')),
    path('api/auth/registration/',include('dj_rest_auth.registration.urls')), 
]