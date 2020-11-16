from django.db import models
from datetime import datetime
from django.contrib.auth.models import User

# Create your models here.
class Portfolio(models.Model):
    user_id = models.IntegerField()
    ticker = models.CharField(max_length=100)
    add_date = models.DateTimeField(blank=True, default=datetime.now)

    def __str__(self):
        return self.ticker
