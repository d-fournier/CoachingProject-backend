from django.db import models
from sport.models import Sport

# Create your models here.
class Level(models.Model):
	title = models.CharField(max_length=100)
	rank = models.PositiveIntegerField()
	sport = models.ForeignKey(Sport, on_delete=models.CASCADE)

	def __str__(self):
		return self.sport.name  + ' : ' + self.title