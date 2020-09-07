from django.db import models


# Create your models here.

class User(models.Model):
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=64)
    age = models.IntegerField()
    gender = models.BooleanField()

    class Meta:
        db_table = 'user'
