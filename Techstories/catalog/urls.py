from django.urls import path
from . import views
from .views import profile

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [    
    path('', views.index, name='index'),
    path('profile/', profile, name='profile'),
    path('profiles/', views.ProfileListView.as_view(), name='profiles'),
    path('profile/<int:pk>', views.profile_detail_view, name='profile-detail'),
    path('post/create/', views.PostCreate.as_view(), name='post-create'),
    path('post/<int:pk>', views.post_detail_view, name='post-detail'),
]