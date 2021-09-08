import base64
import json                    

import requests

# kubectl port-forward -n user1 svc/ocrapp 8080:80 --address 192.168.1.184
#
#api = 'http://localhost:8000/image/text'
api = 'http://k-master.podbox.io:8080/image/text'
#api = 'http://ocrapp.podbox.io/image/text'

#image_file = 'phototest.tif'
#image_file = 'testimage_tiny_color.jpg'
image_file = 'testimage_medium_color.jpg'
#image_file = '/Users/vkraskov/Downloads/IMG_4918.jpg'
#image_file = '/Users/vkraskov/Downloads/IMG_4918-ConvertImage.jpg'

with open(image_file, "rb") as f:
    im_bytes = f.read()        
im_b64 = base64.b64encode(im_bytes).decode("utf8")

headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
  
payload = json.dumps({"image": im_b64, "other_key": "value"})
response = requests.post(api, data=payload, headers=headers)
print(response.text)

#try:
#    data = response.json()     
##    print(data)                
#except requests.exceptions.RequestException:
#    #print(response.text)
#	pass
##except Exception as e:
##    print(e)
