import json                    

import requests

urls = [
		'http://localhost:8000/service/readinessProbe',
		'http://localhost:8000/service/livenessProbe',
		'http://localhost:8000/service/startupProbe',
]

headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
for url in urls:
	response = requests.get(url, headers=headers)
	print(response.text)
