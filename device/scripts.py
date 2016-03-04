import requests
import json
from user.models import UserProfile
from device.models import Device
from django.conf import settings

GCM_SEND_URL = 'https://gcm-http.googleapis.com/gcm/send'

def sendGCMMessage(users,data):
	tokens = []
	for up in users :
		devices = Device.objects.filter(user=up)
		for d in devices :
			tokens.append(d.registration_token)
	headers = {'Authorization':'key='+settings.GCM_API_KEY, 'Content-type':'application/json'}
	payload = json.dumps({'registration_ids':tokens,'data':{'title':data['title'],'body':data['body']}})
	r = requests.post(GCM_SEND_URL, data = payload, headers=headers)
	print(r.status_code)
	print(r.text)
