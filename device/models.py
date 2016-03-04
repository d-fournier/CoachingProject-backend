from user.models import UserProfile
from django.db import models

class Device(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    device_id = models.CharField(max_length=50)
    registration_token = models.CharField(max_length=255)
    name = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
    	unique_together = ('user','device_id')