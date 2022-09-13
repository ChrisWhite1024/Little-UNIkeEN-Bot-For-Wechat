import requests
import json
from basicConfigs import SERVER_IP, SERVER_PORT

HTTP_URL = f"http://{SERVER_IP}:{SERVER_PORT}/v1/"

headers = {
  'Content-Type': 'application/json'
}
# 发送消息
# class Send():

