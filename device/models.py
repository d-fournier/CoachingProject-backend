from gcm.models import AbstractDevice
from user.models import UserProfile
from django.db import models

class Device(AbstractDevice):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    class Meta:
    	unique_together = ('user','dev_id')