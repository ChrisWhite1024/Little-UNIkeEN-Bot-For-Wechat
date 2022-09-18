# 注意版本！
# Flask-SocketIO==4.3.2
# python-engineio==3.14.2 
# python-socketio==4.6.1
from concurrent.futures import thread
import threading
from flask_socketio import socketio
from utils.runtime import PreLoader
from utils.runtime import Runtime

sio = socketio.Client(logger=False, engineio_logger=False)

# 筛选事件上报
def judgeMessage(message):
    if message['CurrentPacket']['Data']['MsgType'] == 1:
        # 收到群消息返回 1
        # 收到私信返回 2
        fromUserName = message['CurrentPacket']['Data']['FromUserName']
        if fromUserName[-9:] == '@chatroom':
            return 1
        return 2
    return -1


# -----------------------------------------------------
# Socketio
# -----------------------------------------------------


@sio.event
def connect():
    print('[L] (main.py)SocketIO：WebSocket服务端已连接')


@sio.on('OnWeChatMsgs')
def OnWeChatMsgs(message):
    ''' 监听Wx消息'''
    print('[L] (main.py)SocketIO：接收到消息事件')
    flag = judgeMessage(message)
    data = message['CurrentPacket']['Data']
    # 群文本消息处理
    if flag == 1:
        msg = message['CurrentPacket']['Data']['Content'].strip()
        for module in runtime.preLoader.CHATROOM_MODULE_LIST:
            if runtime.preLoader.isChatRoomPluginEnabled(module, data['FromUserName']):
                if runtime.preLoader.CHATROOM_MODULE_LIST[module].Plugin.judgeTrigger(msg, data):
                    threading.Thread(target=runtime.preLoader.CHATROOM_MODULE_LIST[module].Plugin.executeEvent, args=(msg, data, runtime), daemon=True).start()
    # 私聊文本消息处理
    if flag == 2:
        msg = message['CurrentPacket']['Data']['Content'].strip()
        for module in runtime.preLoader.USER_MODULE_LIST:
            if runtime.preLoader.isUserPluginEnabled(module):
                if runtime.preLoader.USER_MODULE_LIST[module].Plugin.judgeTrigger(msg, data):
                    threading.Thread(target=runtime.preLoader.USER_MODULE_LIST[module].Plugin.executeEvent, args=(msg, data, runtime), daemon=True).start()
    # print(f'[L] (main.py)SocketIO：消息事件JSON\n\n{message}\n')
    return "OK"


@sio.on('OnWeChatEvents')
def OnWeChatEvents(message):
    ''' 监听Wx事件 '''
    print(message)

# -----------------------------------------------------


def main():
    sio.connect("http://{}:{}".format(runtime.preLoader.getGlobalConfig('SERVER_IP'), runtime.preLoader.getGlobalConfig('SERVER_PORT')), transports=['websocket'])

    sio.wait()

    sio.disconnect()


if __name__ == '__main__':
    runtime = Runtime()
    #preLoader = PreLoader()
    main()
