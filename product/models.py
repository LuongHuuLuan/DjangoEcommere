from django.db import models
from django.conf import settings

# Create your models here.

images_dir = settings.MEDIA_ROOT.joinpath("images")
videos_dir = settings.MEDIA_ROOT.joinpath("videos")

class Product(models.Model):
    name = models.CharField(max_length=255)
    introduce = models.TextField()
    price = models.PositiveIntegerField(default=0)
    quantity = models.PositiveIntegerField(default=0)
    create_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='images_dir', blank=True, null=True)
    video = models.FileField(upload_to='videos_dir', blank=True, null=True)

