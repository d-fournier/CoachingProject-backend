from django.db import models
from django.contrib.auth.models import User
from level.models import Level

# Create your models here.
class UserProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	age = models.PositiveIntegerField()
	city = models.CharField(max_length=50)
	levels = models.ManyToManyField(Level, on_delete=models.CASCADE)
	coachs = models.ManyToManyField('self', symmetrical=False)
	trainee = models.ManyToManyField('self', symmetrical=False)