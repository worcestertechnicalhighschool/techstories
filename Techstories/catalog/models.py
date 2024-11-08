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
    """A typical class defining a model, derived from the Model class."""
    # Fields
    image = models.ImageField()
    title = models.CharField(max_length=20, help_text='Enter post title')
    caption = models.TextField(max_length=100)
    likes = models.PositiveIntegerField(default = 0)
    date = models.DateTimeField(auto_now=True)
    author = models.ForeignKey('Profile', on_delete=models.RESTRICT, null=True)

    # Metadata
    class Meta:
        ordering = ['-caption', '-likes']

    # Methods
    def get_absolute_url(self):
        """Returns the URL to access a particular instance of MyModelName."""
        return reverse('model-detail-view', args=[str(self.id)])

    def __str__(self):
        return self.caption

class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    avatar = models.ImageField(default='default.jpg', upload_to='profile_images')
    posts = models.ManyToManyField(Post, blank=True)
    bio = models.TextField(max_length=100)

    def __str__(self):
        return f"{self.user}"
    
    def save(self, *args, **kwargs):
        super().save()

        img = Image.open(self.avatar.path)

        if img.height > 100 or img.width > 100:
            new_img = (100, 100)
            img.thumbnail(new_img)
            img.save(self.avatar.path)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()