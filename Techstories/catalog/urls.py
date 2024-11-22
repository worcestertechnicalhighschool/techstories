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
    path('profile/<int:pk>/delete', views.UserDelete.as_view(), name='profile-delete'),

    path('post/create/', views.PostCreate.as_view(), name='post-create'),
    path('post/<int:pk>', views.post_detail_view, name='post-detail'),
    path('post/<int:pk>/update/ ', views.PostUpdate.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', views.PostDelete.as_view(), name='post-delete'),

    path('play/<str:audio_file_name>/', views.play_audio, name='play_audio'),

    path('register/', views.register, name='register'),
]