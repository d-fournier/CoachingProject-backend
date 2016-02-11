from django.db import models
from message.models import Message
from user.models import UserProfile

# Create your models here.
class Conversation(models.Model):
	between_users = models.ManyToManyField(UserProfile, blank=False)