from django.db import models

# Create your models here.


class User(models.Model):

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    email = models.EmailField()
    password = models.CharField(max_length=20)


class Scan(models.Model):

    scan_id = models.AutoField(primary_key=True)
    time = models.DateTimeField()
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    region = models.CharField(max_length=200)
    disease = models.CharField(max_length=200)
    result = models.CharField(max_length=50)
