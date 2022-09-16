from typing import Union, Any
from utils.basicEvents import Send
from utils.standardPlugin import StandardPlugin

'''
1. 插件中必须有一个继承自'StandardPlugin'的'Plugin'类
2. 注意需要编写'PLUGIN_INFO'

type: 插件适用范围
1 群聊
2 用户
3 群聊与用户
4 插件关闭
'''

PLUGIN_INFO = {
    'name' : '插件模版',
    'version' : '0.0.1',
    'description' : '除了type外其他键值内容自行决定，用于插件简介的可视化',
    'type' : 3,
}

'''
judgeTrigger 触发器 返回True/False 若返回True则执行executeEvent函数
executeEvent 插件逻辑写在这里，当然，你也可以自定义函数与类使插件功能更加丰富
msg 消息内容
data 消息JSON
'''

class Plugin(StandardPlugin):
    def judgeTrigger(msg:str, data:Any) -> bool:
        return msg == "Hello" 
    def executeEvent(msg:str, data:Any) -> Union[None, str]:
        Send.sendMsg(f"{data['FromUserName']}","Hello World")
        return "OK"

'''
utils.basicEvents中的Send类封装了发送各类消息的方法
Send.sendImage(self, ToUserName, ImagePath) 发送图片,图片地址可以为url和本地地址
Send.sendMsg(self, ToUserName, Content, AtUsers="") 发送消息,暂时不支持@功能,建议将AtUsers项留空
Send.sendAppMsg(self, ToUserName, Content) 发送App消息,可以发送小程序链接

'''