from django.db import models
from user.models import UserProfile
from sport.models import Sport

# Create your models here.
class Group(models.Model):
	name = models.CharField(max_length=100)
	description = models.TextField()
	members = models.ManyToManyField(UserProfile, blank=False)
	sport = models.ForeignKey(Sport, blank=False)
	creation_date = models.DateField(auto_now_add=True,auto_now=False)

	def __str__(self):
		return self.name
