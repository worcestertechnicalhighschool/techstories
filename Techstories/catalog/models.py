from django.db import models
from datetime import datetime, timezone

from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

# Create your models here.
from django.db import models
from django.urls import reverse
from PIL import Image

class Post(models.Model):
    image = models.ImageField(upload_to='post_images')
    title = models.CharField(max_length=20, help_text='Enter post title')
    caption = models.TextField(max_length=10000)
    likes = models.PositiveIntegerField(default = 0)
    date = models.DateTimeField(auto_now=True)
    author = models.ForeignKey('Profile', on_delete=models.RESTRICT, null=True)

    class Meta:
        ordering = ['-caption', '-likes']

    def get_absolute_url(self):
        return reverse('post-detail', args=[str(self.id)])

    def __str__(self):
        return self.caption

class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    avatar = models.ImageField(default='default.jpg', upload_to='profile_images')
    bio = models.TextField(max_length=1000)
    followers = models.ManyToManyField('Profile', blank=True)

    def __str__(self):
        return f"{self.user}"
    
    def save(self, *args, **kwargs):
        super().save()

        img = Image.open(self.avatar.path)

        if img.height > 100 or img.width > 100:
            new_img = (100, 100)
            img.thumbnail(new_img)
            img.save(self.avatar.path)
    
    def get_absolute_url(self):
        return reverse('profile-detail', args=[str(self.id)])

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()