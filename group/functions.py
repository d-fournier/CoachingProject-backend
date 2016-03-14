from group.models import GroupStatus, Group
from django.core.exceptions import ObjectDoesNotExist

def is_user_in_group(user,group):
	try:
		group_status = GroupStatus.objects.get(group=group,user=user)
		if group_status.status!=GroupStatus.PENDING and group_status.status!=GroupStatus.INVITED:
			return True
		return False
	except ObjectDoesNotExist :
		return False

def is_user_in_group_or_pending(user,group):
	try:
		group_status = GroupStatus.objects.get(group=group,user=user)
		return True
	except ObjectDoesNotExist :
		return False


def is_user_admin_in_group(user,group):
	try:
		group_status = GroupStatus.objects.get(group=group,user=user)
		if group_status.status==GroupStatus.ADMIN:
			return True
		return False
	except ObjectDoesNotExist :
		return False

def get_group(pk):
	try :
		return Group.objects.get(pk=pk)
	except ObjectDoesNotExist:
		return None

def get_members(group):
	users = []
	group_status = GroupStatus.objects.filter(group=group)
	for gs in group_status:
		if gs.status!=GroupStatus.PENDING and gs.status!=GroupStatus.INVITED:
			users.append(gs.user)
	return users