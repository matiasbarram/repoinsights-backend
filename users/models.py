from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    github_id = models.IntegerField(null=True, blank=True)
    github_username = models.CharField(max_length=255, null=True, blank=True)
    github_email = models.EmailField(null=True, blank=True)
    github_avatar_url = models.CharField(max_length=255, null=True, blank=True)
    github_access_token = models.CharField(max_length=255, null=True, blank=True)
    github_url = models.CharField(max_length=255, null=True, blank=True)
    github_bio = models.TextField(null=True, blank=True)
    github_company = models.CharField(max_length=255, null=True, blank=True)
    github_location = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.username
