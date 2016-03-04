import requests
from user.models import UserProfile
from device.models import Device
from django.conf import settings

GCM_SEND_URL = 'https://gcm-http.googleapis.com/gcm/send'

def sendGCMMessage(users,data):
	tokens = []
	for up in users :
		tokens.append(Device.objects.get(user=up).reg_token)
	headers = {'Authorization':'key='+settings.GCM_API_KEY, 'Content-type':'application/json'}
	payload = {'to':tokens,'data':{'title':data['title'],'body':data['body']}}
	r = requests.post(GCM_SEND_URL, data = payload, headers=headers)
