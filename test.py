import requests
import json
headers = {'Content-Type': 'application/json'}
url = 'http://43.138.112.209:8081/v1/LuaApiCaller?funcname=SendImage&timeout=10&wxid=wxid_sfxvc2xx54rl12'

payload = json.dumps({"ToUserName":"wxid_dn9wlcqqs5dy22","ImageUrl":"https://file.chriswhite.to/%E4%B8%98%E4%B8%98%E4%BA%BA%E4%B9%9F%E8%83%BD%E6%90%9E%E6%87%82%E7%9A%84%E5%85%AC%E5%A4%A7%E7%BD%91%E5%AE%89%E8%AF%BE%E7%A8%8B%E6%8C%87%E5%8D%97%E4%BD%BF%E7%94%A8%E6%95%99%E7%A8%8B/image-20220801202920742.png"})
response = requests.request("POST", url, headers=headers, data=payload)
if response.json() == None:
    print("e")
