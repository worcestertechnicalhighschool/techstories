from django.urls import path
from . import views
from .views import profile

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('profile/', profile, name='users-profile'),    
    path('', views.index, name='index'),
]