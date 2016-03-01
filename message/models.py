from django.db import models
from user.models import UserProfile
from relation.models import Relation
from group.models import Group

# Create your models here.
class Message(models.Model):
	content = models.TextField()
	from_user = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True)
	to_relation = models.ForeignKey(Relation, on_delete=models.CASCADE, null=True)
	to_group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True)
	time = models.DateTimeField(auto_now_add=True)
	is_pinned=models.BooleanField()

