from django.db import models
from user.models import UserProfile
from relation.models import Relation
from group.models import Group

def message_directory_path(instance, filename):
	return 'messages/{0}_{1}'.format(instance.from_user.id,filename)

# Create your models here.
class Message(models.Model):
	content = models.TextField()
	from_user = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True)
	to_relation = models.ForeignKey(Relation, on_delete=models.CASCADE, null=True, blank=True)
	to_group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True, blank=True)
	time = models.DateTimeField(auto_now_add=True)
	is_pinned=models.BooleanField(default=False)
	associated_file = models.FileField(upload_to=message_directory_path, default=None, null=True, blank=True)

