from django.db import models
from ckeditor.fields import RichTextField
from datetime import datetime

# Create your models here.
class Francois(models.Model):
    first_name = models.CharField(max_length=300)
    designation = models.CharField(max_length=300)
    about_para1 = RichTextField()
    about_me_side_bar = RichTextField()
    about_blockquote = RichTextField()
    about_short = RichTextField()
    facebook_link = models.URLField(max_length=100, blank=True)
    twitter_link = models.URLField(max_length=100, blank=True)
    instagram_link = models.URLField(max_length=100, blank=True)
    last_update = models.DateTimeField(blank=True, default=datetime.now)
    home_images1 = models.ImageField(upload_to='photos/%Y/%m/%d/')
    home_images2 = models.ImageField(upload_to='photos/%Y/%m/%d/')
    home_images3 = models.ImageField(upload_to='photos/%Y/%m/%d/')
    home_images4 = models.ImageField(upload_to='photos/%Y/%m/%d/')
    home_images5 = models.ImageField(upload_to='photos/%Y/%m/%d/')
    home_images6 = models.ImageField(upload_to='photos/%Y/%m/%d/')
    home_images7 = models.ImageField(upload_to='photos/%Y/%m/%d/')
    home_images8 = models.ImageField(upload_to='photos/%Y/%m/%d/')
    about_side_bar = models.ImageField(upload_to='photos/%Y/%m/%d/')

    def __str__(self):
        return self.first_name
