import websocket,time,json,requests,os,urllib
from bs4 import BeautifulSoup

from utils.basicHttpEvent import *
from utils.basicConfigs import *
from utils.basicWsEvent import *

from plugins.news import *

ROOT_PATH = os.path.dirname(os.path.realpath(__file__))
RESOURCES_PATH = ROOT_PATH+"/resources"

GroupPluginList=[
    ShowNews,
]

websocket._logging._logger.level = -99

def getid():
    return time.strftime("%Y%m%d%H%M%S")

#控制台消息
def output(msg):
    now=time.strftime("%Y-%m-%d %X")
    print(f'[{now}]:{msg}')

def debug_switch():
    qs={
        'id':getid(),
        'type':DEBUG_SWITCH,
        'content':'off',
        'wxid':'ROOT',
    }
    return json.dumps(qs)

#初始化
def on_open(ws):
    ws.send(send_wxuser_list())

def on_error(ws,error):
    output(f'on_error:{error}')

def on_close(ws):
    output("closed")

def welcome_join(msgJson):
    output(f'收到消息:{msgJson}')
    if '邀请' in msgJson['content']['content']:
        roomid=msgJson['content']['id1']
        nickname=msgJson['content']['content'].split('"')[-2]
        ws.send(send_msg(f'欢迎新进群的老色批',roomid=roomid,wxid='null',nickname=nickname))

def handleMsg_cite(msgJson):
    # 处理带引用的文字消息
    msgXml=msgJson['content']['content'].replace('&amp;','&').replace('&lt;','<').replace('&gt;','>')
    soup=BeautifulSoup(msgXml,'lxml')
    msgJson={
        'content':soup.select_one('title').text,
        'id':msgJson['id'],
        'id1':msgJson['content']['id2'],
        'id2':'wxid_fys2fico9put22',
        'id3':'',
        'srvid':msgJson['srvid'],
        'time':msgJson['time'],
        'type':msgJson['type'],
        'wxid':msgJson['content']['id1']
    }
    handle_recv_msg(msgJson)
    
def handle_nick(j):
    data=j.content
    i=0
    for d in data:
        output(f'nickname:{d.nickname}')
        i+=1

def handle_memberlist(j):
    data=j.content
    i=0
    for d in data:
        output(f'roomid:{d.roomid}')
        i+=1

def handle_wxuser_list(j):
    # i=0
    # for item in j['content']:
    #     i+=1
    #     output(f"{i} {item['wxid']} {item['name']}")
    output('启动完成')

def heartbeat(msgJson):
    output(msgJson['content'])

#######################################################################################################

def handle_recv_msg(msgJson):
    output(f'收到消息:{msgJson}')
    keyword=msgJson['content'].replace('\u2005','').strip()
    if '@chatroom' in msgJson['wxid']:
        roomid=msgJson['wxid'] #群id
        senderid=msgJson['id1'] #个人id
        flag = 1
    else:
        roomid=None
        nickname='null'
        senderid=msgJson['wxid'] #个人id
        flag = 2
    nickname=get_member_nick(roomid,senderid)

    if flag == 1:
        for event in GroupPluginList:
            event: StandardPlugin
            if event.judgeTrigger(keyword, msgJson):
                ret = event.executeEvent(keyword, msgJson)
                if ret != None:
                    return ret

#######################################################################################################

def on_message(ws,message):
    j=json.loads(message)
    resp_type=j['type']
    # switch结构
    action={
        CHATROOM_MEMBER_NICK:handle_nick,
        PERSONAL_DETAIL:handle_recv_msg,
        AT_MSG:handle_recv_msg,
        DEBUG_SWITCH:handle_recv_msg,
        PERSONAL_INFO:handle_recv_msg,
        TXT_MSG:handle_recv_msg,
        PIC_MSG:handle_recv_msg,
        CHATROOM_MEMBER:handle_memberlist,
        RECV_PIC_MSG:handle_recv_msg,
        RECV_TXT_MSG:handle_recv_msg,
        #RECV_TXT_CITE_MSG:handleMsg_cite,
        HEART_BEAT:heartbeat,
        USER_LIST:handle_wxuser_list,
        GET_USER_LIST_SUCCSESS:handle_wxuser_list,
        GET_USER_LIST_FAIL:handle_wxuser_list,
        #JOIN_ROOM:welcome_join,
    }
    action.get(resp_type,print)(j)

# websocket.enableTrace(True)
ws=websocket.WebSocketApp(SERVER,on_open=on_open,on_message=on_message,on_error=on_error,on_close=on_close)
ws.run_forever()
