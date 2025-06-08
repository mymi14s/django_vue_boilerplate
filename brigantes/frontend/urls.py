from django.urls import path
from .views import frontend, get_csrf_token

app_name = 'frontend'

urlpatterns = [
    path('', frontend, name='frontend'),
    path('get_csrf_token', get_csrf_token, name='get_csrf_token'),
]