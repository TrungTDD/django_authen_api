from django.contrib.auth.models import User
from django.db import models
from django.db.models.fields.related import ForeignKey

# Create your models here.


class Task(models.Model):
    title = models.CharField(max_length=256)
    description = models.TextField()
    user = ForeignKey(User, on_delete=models.CASCADE, related_name="task")
