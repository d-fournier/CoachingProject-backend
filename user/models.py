from django.db import models
from django.contrib.auth.models import User
from level.models import Level

# Create your models here.
class UserProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	age = models.PositiveIntegerField()
	city = models.CharField(max_length=50)
	levels = models.ManyToManyField(Level)
	coachs = models.ManyToManyField('self', related_name='%(class)s_coachs', symmetrical=False)
	trainees = models.ManyToManyField('self', related_name='%(class)s_trainees', symmetrical=False)