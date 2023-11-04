from django.db import models
from django.contrib.auth.models import User

class Review(models.Model):
    brewery_id = models.UUIDField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()
    description = models.TextField()
    timestamp = models.DateTimeField(auto_now=True)