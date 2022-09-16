# 注意版本！
# Flask-SocketIO==4.3.2
# python-engineio==3.14.2 
# python-socketio==4.6.1
import importlib
from time import sleep
from flask_socketio import socketio
from utils.preLoader import PreLoader

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

        return 2
    return -1


# -----------------------------------------------------
# Socketio
# -----------------------------------------------------


@sio.event
def connect():
    print('[L] (main.py)SocketIO：WebSocket服务器已连接')


@sio.on('OnWeChatMsgs')
def OnWeChatMsgs(message):
    ''' 监听Wx消息'''
    print('[L] (main.py)SocketIO：接收到消息事件')
    flag = judgeMessage(message)
    data = message['CurrentPacket']['Data']
    # 群文本消息处理

    # 私聊文本消息处理
    if flag == 2:
        msg = message['CurrentPacket']['Data']['Content'].strip()

        if preLoader.USER_MODULE_LIST['template.py'].Plugin.judgeTrigger(msg, data):
            preLoader.USER_MODULE_LIST['template.py'].Plugin.executeEvent(msg, data)
        sleep(3)
        if preLoader.USER_MODULE_LIST['template1.py'].Plugin.judgeTrigger(msg, data):
            preLoader.USER_MODULE_LIST['template1.py'].Plugin.executeEvent(msg, data)
        '''
        for event in PrivatePluginList:
            event: StandardPlugin
            if event.judgeTrigger(msg, data):
                ret = event.executeEvent(msg, data)
                if ret != None:
                    return ret
        '''
    print(f'[L] (main.py)SocketIO：消息事件JSON\n\n{message}\n')
    return "OK"


@sio.on('OnWeChatEvents')
def OnWeChatEvents(message):
    ''' 监听Wx事件 '''
    # print(message)

# -----------------------------------------------------


def main():
    sio.connect("http://{}:{}".format(preLoader.getGlobalConfig('SERVER_IP'), preLoader.getGlobalConfig('SERVER_PORT')), transports=['websocket'])

    sio.wait()

    sio.disconnect()


if __name__ == '__main__':
    '''
    module_spec = importlib.util.spec_from_file_location('helloWorld', PLUGINS_PATH + '/helloWorld.py')
    module = importlib.util.module_from_spec(module_spec)
    module_spec.loader.exec_module(module)
    print(dir(module))
    PluginList = os.listdir(PLUGINS_PATH)
    print(PluginList)
    '''
    preLoader = PreLoader()
    main()
