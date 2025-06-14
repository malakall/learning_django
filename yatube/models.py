from django.db import models
from .validators import validation

from django.contrib.auth.models import User

class Group(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    user_name = models.CharField(max_length=15)
    image = models.ImageField(upload_to='posts/', blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # автор записи
    

    def __str__(self):
        return self.name


class Contact(models.Model):
    name = models.TextField(max_length=100, verbose_name="ваше имя", validators=[validation])
    email = models.EmailField(max_length=30, verbose_name="ваш email", validators=[validation])
    text = models.TextField(verbose_name="текст обращения", validators=[validation])

    def __str__(self):
        return self.name
    