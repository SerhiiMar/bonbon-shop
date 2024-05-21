from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    city = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.username} ({self.first_name} {self.last_name})"


