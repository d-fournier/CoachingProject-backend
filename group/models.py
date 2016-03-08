from django.db import models
from user.models import UserProfile
from sport.models import Sport

# Create your models here.
class Group(models.Model):
	name = models.CharField(max_length=100)
	description = models.TextField()
	sport = models.ForeignKey(Sport, blank=False)
	city = models.CharField(max_length=60)
	creation_date = models.DateField(auto_now_add=True,auto_now=False)
	private = models.BooleanField(default=False)

	def __str__(self):
		return self.name

class GroupStatus(models.Model):
	group = models.ForeignKey(Group, on_delete=models.CASCADE)
	user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

	ADMIN = 'ADM'
	MEMBER = 'MEM'
	PENDING = 'PEN'
	INVITED = 'INV'
	user_status = (
        (ADMIN, 'Admin'),
        (MEMBER, 'Member'),
        (PENDING, 'Pending'),
        (INVITED,'Invited')
    )
	status= models.CharField(max_length=3,choices=user_status, blank=False, null=False)

	class Meta:
		unique_together = ('group','user')
