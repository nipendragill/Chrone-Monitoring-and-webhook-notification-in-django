from django.db import models
from .check import CheckDetails
from datetime import timedelta, time
from ..error import Error


class CheckTrack(models.Model):

    check_id = models.ForeignKey(CheckDetails, on_delete=models.CASCADE())
    cron_expected_run_time = models.DateTimeField(auto_now=True)
    cron_max_run_time = models.DateTimeField(auto_now=True)
    is_cron_run = models.BooleanField(default=True)

    def crone_expected_run_time(self, time_in_second= None):
        if time_in_second is None:
            return False
        cron_max_run_time = self.cron_expected_run_time + timedelta(seconds=time_in_second)


