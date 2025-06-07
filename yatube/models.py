from django.db import models

from django.contrib.auth.models import User

class Group(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # автор записи

    def __str__(self):
        return self.name
