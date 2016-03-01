from django.db import models
from user.models import UserProfile

# Create your models here.
class Group(models.Model):
	name = models.CharField(max_length=100)
	description = models.TextField()
	users = models.ManyToManyField(UserProfile, blank=False)

	def __str__(self):
		return self.name
