from django.db import models

# Create your models here.
class blogpost(models.Model):
    title = models.CharField(max_length=150)
    des = models.TextField(max_length=100)