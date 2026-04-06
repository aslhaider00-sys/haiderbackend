from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=75)
    # body = models.TextField()
    # slug = models.SlugField()
    date = models.DateTimeField(auto_now_add=True)
    banner = models.ImageField(default='fallback.png')
    demonstration = models.FileField(default='sign.mp4')
    category = models.CharField(max_length=75)
    uploader = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    #bali rereturn/ display kapag  laman pagnag >>> Post.objects.all() JUST OGNORE NALANNG
    def __str__(self):
        return self.title