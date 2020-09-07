from django.db import models


# Create your models here.

class Staff(models.Model):
    name = models.CharField(max_length=32)
    age = models.IntegerField()
    gender = models.BooleanField()

    class Meta:
        db_table = 'staff'
