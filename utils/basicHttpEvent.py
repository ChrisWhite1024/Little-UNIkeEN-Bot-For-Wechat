import json, requests
from main import getid
from basicConfigs import *


#发送消息
def send(uri,data):
    base_data={
        'id':getid(),
        'type':'null',
        'roomid':'null',
        'wxid':'null',
        'content':'null',
        'nickname':'null',
        'ext':'null',
    }
    base_data.update(data)
    url=f'http://{ip}:{port}/{uri}'
    res=requests.post(url,json={'para':base_data},timeout=5)
    return res.json()


# 获取指定群的成员的昵称 或 微信好友的昵称
def get_member_nick(roomid,wxid):
    uri='api/getmembernick'
    data={
        'type':CHATROOM_MEMBER_NICK,
        'wxid':wxid,
        'roomid':roomid or 'null'
    }
    respJson=send(uri,data)
    return json.loads(respJson['content'])['nick']


# 获取本机器人的信息
def get_personal_info():
    uri='/api/get_personal_info'
    data={
        'id':getid(),
        'type':PERSONAL_INFO,
        'content':'op:personal info',
        'wxid':'null',
    }
    respJson=send(uri,data)
    print(respJson)