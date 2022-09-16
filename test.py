import requests
import json

url = "http://bbb:8081/v1/LuaApiCaller?funcname=InitWxids&timeout=10&wxid=wxid_sfxvc2xx54rl1"

payload = json.dumps({
  "CurrentWxcontactSeq": 0,
  "CurrentChatRoomContactSeq": 0
})
headers = {
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.json())