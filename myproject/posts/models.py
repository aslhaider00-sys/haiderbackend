from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=75)
    body = models.TextField()
    slug = models.SlugField()
    date = models.DateTimeField(auto_now_add=True)
    banner = models.ImageField(upload_to='images/',default='images/defaulthandsign.png')
    demonstration = models.FileField(upload_to='videos/',default='videos/defaulthandsignvideo.mp4')
    category = models.CharField(max_length=75)
    difficulty = models.CharField(max_length=75, default='easy')
    # uploader = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
 