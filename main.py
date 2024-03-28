# 注意版本！
# Flask-SocketIO==4.3.2
# python-engineio==3.14.2 
# python-socketio==4.6.1
from concurrent.futures import thread
from flask_socketio import socketio
from utils.runtime import PreLoader
from utils.runtime import Runtime
from concurrent.futures import ThreadPoolExecutor

sio = socketio.Client(logger=False, engineio_logger=False)
executor = ThreadPoolExecutor(max_workers=10)

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

def judgeEvent(message):
    fromUserName = message['CurrentPacket']['Data'].get("FromUserName", False)
    if not fromUserName:
        return -1
    if fromUserName[-9:] == '@chatroom':
        return 1
    return 2

def handle_message(flag, msg, data, module_list, is_enabled_func):
    for module in module_list:
        if not is_enabled_func(module, data['FromUserName']):
            continue
        # 将judgeTrigger的执行放在一个单独的线程中
        future = executor.submit(module.Plugin.judgeTrigger, msg, data)
        if future.result():
            executor.submit(module.Plugin.executeEvent, msg, data, runtime)


# -----------------------------------------------------
# Socketio
# -----------------------------------------------------


@sio.event
def connect():
    for module in runtime.preLoader.CHATROOM_MODULE_LIST:
        executor.submit(module.Plugin.executeEvent, runtime)
    print('[L] (main.py)SocketIO：WebSocket服务端已连接')


@sio.on('OnWeChatMsgs')
def OnWeChatMsgs(message):
    ''' 监听Wx消息'''
    print('[L] (main.py)SocketIO：接收到消息事件')
    flag = judgeMessage(message)
    data = message['CurrentPacket']['Data']
    msg = message['CurrentPacket']['Data']['Content'].strip()
    # 群文本消息处理
    if flag == 1:
        handle_message(flag, msg, data, runtime.preLoader.CHATROOM_MODULE_LIST, runtime.preLoader.isChatRoomPluginEnabled)
    # 私聊文本消息处理
    if flag == 2:
        handle_message(flag, msg, data, runtime.preLoader.USER_MODULE_LIST, runtime.preLoader.isUserPluginEnabled)
    print(f'[L] (main.py)SocketIO：消息JSON\n\n{message}\n')
    return "OK"


@sio.on('OnWeChatEvents')
def OnWeChatEvents(message):
    ''' 监听Wx事件 '''
    flag = judgeEvent(message)
    data = message['CurrentPacket']['Data']
    msg = ""
    # 群文本消息处理
    if flag == 1:
        handle_message(flag, msg, data, runtime.preLoader.CHATROOM_MODULE_LIST, runtime.preLoader.isChatRoomPluginEnabled)
    # 私聊文本消息处理
    if flag == 2:
        handle_message(flag, msg, data, runtime.preLoader.USER_MODULE_LIST, runtime.preLoader.isUserPluginEnabled)
    print(f'[L] (main.py)SocketIO：事件JSON\n\n{message}\n')

# -----------------------------------------------------


def main():
    sio.connect("http://{}:{}".format(runtime.preLoader.getGlobalConfig('SERVER_IP'), runtime.preLoader.getGlobalConfig('SERVER_PORT')), transports=['websocket'])
    sio.wait()
    sio.disconnect()


if __name__ == '__main__':
    runtime = Runtime()
    main()
