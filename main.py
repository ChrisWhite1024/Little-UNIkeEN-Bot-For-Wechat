# 注意版本！
# Flask-SocketIO==4.3.2
# python-engineio==3.14.2 
# python-socketio==4.6.1
import importlib
from ntpath import join
from threading import Timer
from flask_socketio import socketio
from plugins.helloWorld import *
from utils.standardPlugin import StandardPlugin
from utils.basicConfigs import *

GroupPluginList = [ # 指定群启用插件

]

PrivatePluginList = [ # 私聊启用插件
    HelloWorld,
]

# standard Python
sio = socketio.Client(logger=False, engineio_logger=False)

# SocketIO Client
# sio = socketio.AsyncClient(logger=True, engineio_logger=True)

# 筛选事件上报
def judgeMessage(message):
    if message['CurrentPacket']['Data']['MsgType'] == 1:
        # 收到群消息返回 1
        # 收到私信返回 2
        fromUserName = message['CurrentPacket']['Data']['FromUserName']
        if fromUserName.endswith('@chatroom') and fromUserName[ : -9] in APPLY_GROUP_ID:
            return 1
        return 2
    return -1


# -----------------------------------------------------
# Socketio
# -----------------------------------------------------


@sio.event
def connect():
    print('connected to server')


@sio.on('OnWeChatMsgs')
def OnWeChatMsgs(message):
    ''' 监听Wx消息'''
    flag = judgeMessage(message)
    data = message['CurrentPacket']['Data']
    # 群文本消息处理
    if flag == 1:
        msg = message['CurrentPacket']['Data']['Content'].strip()
        for event in GroupPluginList:
            event: StandardPlugin
            if event.judgeTrigger(msg, data):
                ret = event.executeEvent(msg, data)
                if ret != None:
                    return ret
    # 私聊文本消息处理
    elif flag==2:
        msg = message['CurrentPacket']['Data']['Content'].strip()
        for event in PrivatePluginList:
            event: StandardPlugin
            if event.judgeTrigger(msg, data):
                ret = event.executeEvent(msg, data)
                if ret != None:
                    return ret
    print(message)
    return "OK"


@sio.on('OnWeChatEvents')
def OnWeChatEvents(message):
    ''' 监听Wx事件 '''
    print(message)

# -----------------------------------------------------


def main():
    sio.connect(f"http://{SERVER_IP}:{SERVER_PORT}", transports=['websocket'])

    sio.wait()
    # Cleanup
    sio.disconnect()


if __name__ == '__main__':
    module_spec = importlib.util.spec_from_file_location('helloWorld', PLUGINS_PATH + '/helloWorld.py')
    module = importlib.util.module_from_spec(module_spec)
    module_spec.loader.exec_module(module)
    print(dir(module))
    main()
