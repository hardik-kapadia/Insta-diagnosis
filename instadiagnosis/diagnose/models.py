from distutils.command.upload import upload
from django.db import models
from django.contrib.auth.models import User


class Scan(models.Model):

    scan_id = models.AutoField(primary_key=True)
    time = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, default="tempo",
                             on_delete=models.CASCADE, null=True)
    disease = models.CharField(max_length=200)
    result = models.CharField(max_length=50, blank=True)
    scan = models.ImageField(upload_to='scans')
