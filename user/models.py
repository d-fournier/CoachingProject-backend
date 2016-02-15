from django.db import models
from django.contrib.auth.models import User
from level.models import Level

# Create your models here.
class UserProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	displayName = models.CharField(max_length=50)
	age = models.PositiveIntegerField()
	isCoach = models.BooleanField(default=False)
	city = models.CharField(max_length=50)
	description = models.TextField(max_length=400, blank=True)
	levels = models.ManyToManyField(Level, blank=True)

	def __str__(self):
		return self.user.username