import requests
import json
from user.models import UserProfile
from message.serializers import MessageReadSerializer
from relation.serializers import RelationReadSerializer
from group.serializers import GroupReadSerializer
from device.models import Device
from django.conf import settings

GCM_SEND_URL = 'https://gcm-http.googleapis.com/gcm/send'

def sendGCMNewMessage(users,message):
	data = {}
	serial = MessageReadSerializer(message)
	data['content'] = serial.data
	data['type']='message_new'
	sendToGCM(users=users,data=data)


def sendGCMCoachingResponse(users, relation):
	data = {}
	serial = RelationReadSerializer(relation)
	data['content'] = serial.data
	data['type']='coaching_response'
	sendToGCM(users=users,data=data)

def sendGCMCoachingCreation(users,relation):
	data = {}
	serial = RelationReadSerializer(relation)
	data['content'] = serial.data
	data['type']='coaching_new'
	sendToGCM(users=users,data=data)

def sendGCMCoachingEnd(users,relation):
	data = {}
	serial = RelationReadSerializer(relation)
	data['content'] = serial.data
	data['type']='coaching_end'
	sendToGCM(users=users,data=data)

def sendGCMGroupInvite(users,group):
	data = {}
	serial = GroupReadSerializer(group)
	data['content'] = serial.data
	data['type']='group_invitation'
	sendToGCM(users=users,data=data)

def sendGCMGroupJoin(users,group):
	data = {}
	serial = GroupReadSerializer(group)
	data['content'] = serial.data
	data['type']='group_join'
	sendToGCM(users=users,data=data)

def sendGCMGroupJoinAccepted(users,group):
	data = {}
	serial = GroupReadSerializer(group)
	data['content'] = serial.data
	data['type']='group_join_accepted'
	sendToGCM(users=users,data=data)
	

def sendToGCM(users,data):
	tokens = []
	print(users)
	for up in users :
		devices = Device.objects.filter(user=up)
		for d in devices :
			tokens.append(d.registration_token)
	headers = {'Authorization':'key='+settings.GCM_API_KEY, 'Content-type':'application/json'}
	if tokens :
		payload = json.dumps({'registration_ids':tokens,'data':data})
		r = requests.post(GCM_SEND_URL, data=payload, headers=headers)
		print('STATUS CODE GCM : \n' + str(r.status_code))
		print('RESPONSE FROM GCM : \n' + r.text)
		response = json.loads(r.text)
		index = 0
		for res in response['results']:
			if 'error' in res:
				token = tokens[index]
				devices_to_delete = Device.objects.filter(registration_token=token)
				for d in devices_to_delete:
					d.delete()
			index += 1
			
