from django.contrib.auth.models import User
from django.db import models

class AuthorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    avatar = models.ImageField(upload_to='authors/avatars/', default='default_avatar.png')
    website = models.URLField(blank=True, null=True)
    
    def __str__(self):
        return self.user.username

