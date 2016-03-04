from user.models import UserProfile
from django.db import models

class Device(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    dev_id = models.CharField(max_length=50, unique=True)
    reg_token = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
    	unique_together = ('user','dev_id')