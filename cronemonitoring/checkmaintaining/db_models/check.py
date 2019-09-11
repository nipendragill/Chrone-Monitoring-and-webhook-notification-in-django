from django.db import models
from ..models import User


class CheckDetails(models.Model):

    request_choices = (
        ('post', 'POST'),
        ('get', 'GET'),
        ('delete', 'DELETE'),
        ('put', 'PUT')
    )
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=200)
    url = models.URLField(max_length=300)
    arrival_time = models.FloatField()
    waiting_time = models.FloatField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE())
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE())
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
