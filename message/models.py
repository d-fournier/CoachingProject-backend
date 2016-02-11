from django.db import models
from user.models import UserProfile

# Create your models here.
class Message(models.Model):
	content = models.TextField()
	from_user = models.ForeignKey(UserProfile, on_delete=models.SET_DEFAULT, default=-1)