from django.db import models
from django.contrib.auth.models import User


def avatar_upload_path(instance, filename):
    return f'avatars/{instance.user.username}/{filename}'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(max_length=300, blank=True)
    avatar = models.ImageField(upload_to=avatar_upload_path, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}'s profile"

    def get_avatar_url(self):
        if self.avatar:
            return self.avatar.url
        return None