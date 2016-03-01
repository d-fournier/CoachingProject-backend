from django.db import models
from user.models import UserProfile
from sport.models import Sport

# Create your models here.
class Relation(models.Model):
	coach = models.ForeignKey(UserProfile,related_name='%(class)s_coach', blank=False)
	trainee = models.ForeignKey(UserProfile,related_name='%(class)s_trainee', blank=False)
	requestStatus = models.NullBooleanField()
	sport = models.ForeignKey(Sport, blank=False)
	comment = models.TextField(blank=True)
	date =  models.DateField(auto_now=False, auto_now_add=True)

	class Meta:
		unique_together=('coach','trainee','sport',)

	def __str__(self):
		return self.coach.user.username+' <-> '+self.trainee.user.username
