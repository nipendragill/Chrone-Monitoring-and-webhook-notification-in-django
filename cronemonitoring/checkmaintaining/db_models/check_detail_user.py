from django.db import models
from .check import CheckDetails
from datetime import timedelta, time, datetime
from ..error import Error
from .check import CheckDetails
from ..models import User


class CheckTrack(models.Model):
    request_choices = (
        ('post', 'POST'),
        ('get', 'GET'),
        ('delete', 'DELETE'),
        ('put', 'PUT')
    )
    check = models.ForeignKey(CheckDetails, on_delete=models.CASCADE())
    request_type = models.CharField(max_length=10, choices=request_choices)
    prev_hitted_at = models.DateTimeField(auto_now_add=True)
    latest_hitted_at = models.DateTimeField(auto_now=True)
    latest_hit_by = models.ForeignKey(User, on_delete=models.CASCADE())
    data_in_request_body = models.TextField(max_length=256)




