from django.db import models
from user.models import UserProfile

# Create your models here.
class Relation(models.Model):
	coach = models.ForeignKey(UserProfile,related_name='%(class)s_coach', blank=False)
	trainee = models.ForeignKey(UserProfile,related_name='%(class)s_trainee', blank=False)
