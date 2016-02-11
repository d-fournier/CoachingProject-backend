from django.db import models
from user.models import UserProfile
from conversation.models import Conversation

# Create your models here.
class Message(models.Model):
	content = models.TextField()
	from_user = models.ForeignKey(UserProfile, on_delete=models.SET_DEFAULT, default=-1)
	to_conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, blank=False)