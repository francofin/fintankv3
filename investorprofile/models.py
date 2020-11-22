from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.
class Portfolio(models.Model):
    user_id = models.IntegerField()
    ticker = models.CharField(max_length=100)
    add_date = models.DateTimeField(blank=True, default=datetime.now)

    def __str__(self):
        return self.ticker

class Portfolio_2(models.Model):
    ticker = models.CharField(max_length=15)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='investor', null=True)

    def __str__(self):
        return self.ticker
