from django.db import models

# Create your models here.
class Image(models.Model):
    image_url = models.CharField(max_length=255)