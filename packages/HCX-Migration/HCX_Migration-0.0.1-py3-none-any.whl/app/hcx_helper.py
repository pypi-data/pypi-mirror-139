from typing import Dict
import requests
from requests.auth import HTTPBasicAuth

class HcxServer:
    def __init__(self,username,password,hostname) -> None:
        self.username = username
        self.password = password
        self.hostname = hostname
        self.auth = HTTPBasicAuth(self.username, self.password)
        pass
    
    def Estanlish_hcx_Connection(self):
        api_url = 'https: //{}/hybridity/api/sessions'.format(self.hostname)
        headers = {
			'Content-Type': 'application/json',
		   }
		response = requests.request('POST', api_url, headers=headers, verify=False, auth=self.auth)
        if response.status_code == 200:
            HcxAuthToken = response.headers.get('x-hm-authorization')
            HCXheaders = { "x-hm-authorization" : HcxAuthToken,"Content-Type":"application/json","Accept":"application/json"}
            HcxConnection = { 'Server': "https://{}/hybridity/api".format(self.hostname),'headers':HCXheaders}
        else:
            print("Can't Connect the Hcx Server")

    def Http_Api_Requestor(self, payload, method):
		"""
		Helper method for REST API Manager.
		:type   api_path: :class:`str`
		:param  api_path:  api_path
		:type   payload: :class:`str`
		:param  payload:  payload
		:type   method: :class:`str`
		:param  method:  method
		:rtype  :class:`str`
		:return
		"""
		api_url = 'https: //{}  /hybridity/api/sessions'.format(self.hostname)
		headers = {
			'Content-Type': 'application/json',
		   }
		response = requests.request(method, api_url, headers=headers, data = payload, verify=False, auth=self.auth)
		if (method == 'PUT') or (method == 'POST') or (method == 'DELETE'):
			return response.json()
		return (response.json()['results'] if 'results' in response.json() else response.json())