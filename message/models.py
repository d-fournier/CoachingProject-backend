from django.db import models
from user.models import UserProfile
from relation.models import Relation

# Create your models here.
class Message(models.Model):
	content = models.TextField()
	from_user = models.ForeignKey(UserProfile, on_delete=models.SET_DEFAULT, default=-1)
	to_relation = models.ForeignKey(Relation, on_delete=models.CASCADE, null=False, blank=True)
	time = models.DateTimeField(auto_now_add=True)