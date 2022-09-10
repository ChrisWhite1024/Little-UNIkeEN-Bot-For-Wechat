import json, websocket
from main import getid, output, ws
from basicConfigs import *


def destroy_all():
    qs={
        'id':getid(),
        'type':DESTROY_ALL,
        'content':'none',
        'wxid':'node',
    }
    return json.dumps(qs)


'''
获取微信通讯录用户名字和wxid
获取微信通讯录好友列表
'''
def send_wxuser_list():
    qs={
        'id':getid(),
        'type':USER_LIST,
        'content':'user list',
        'wxid':'null',
    }
    return json.dumps(qs)


#发送消息
def send_msg(msg,wxid='null',roomid=None,nickname='null'):
    if msg.endswith('.png'):
        msg_type=PIC_MSG
        if roomid:
            wxid=roomid
            roomid=None
            nickname='null'
    elif roomid:
        msg_type=AT_MSG
    else:
        msg_type=TXT_MSG
        nickname='null'
    if roomid==None:
        roomid='null'
    qs={
        'id':getid(),
        'type':msg_type,
        'roomid':roomid,
        'wxid':wxid,
        'content':msg,
        'nickname':nickname,
        'ext':'null'
    }
    output(f'发送消息: {qs}')
    ws.send(json.dumps(qs))


def get_chat_nick_p(roomid):
    qs={
        'id':getid(),
        'type':CHATROOM_MEMBER_NICK,
        'content':roomid,
        'wxid':'ROOT',
    }
    return json.dumps(qs)

#获取群聊成员列表
def get_chatroom_memberlist():
    qs={
        'id':getid(),
        'type':CHATROOM_MEMBER,
        'wxid':'null',
        'content':'op:list member',
    }
    return json.dumps(qs)


def get_personal_detail(wxid):
    qs={
        'id':getid(),
        'type':PERSONAL_DETAIL,
        'content':'op:personal detail',
        'wxid':wxid,
    }
    return json.dumps(qs)