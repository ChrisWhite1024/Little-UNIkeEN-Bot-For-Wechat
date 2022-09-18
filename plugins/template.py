from typing import Union, Any
from utils.runtime import Runtime
from utils.standardPlugin import StandardPlugin
# from utils.basicEvents import Send 

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
    'version' : '0.3.9',
    'description' : '除了type外其他键值内容自行决定，用于插件简介的可视化',
    'author' : '作者写在这里',
    'type' : 4,
}

'''
judgeTrigger 触发器 返回True/False 若返回True则执行executeEvent方法
executeEvent 插件逻辑写在这里，这里也是插件运行的起点，当然，你也可以自定义函数与类使插件功能更加丰富
msg 消息内容 与data['Content']相同
data 消息JSON
Example.

私信消息
{
    'MsgId': 1132550320, 'FromUserName': 'zhanshen9045', 
    'ToUserName': 'wxid_sfxvc2xx54rl12', 'MsgType': 1, 
    'Content': 'suki', 'Status': 3, 'ImgStatus': 1, 
    'ImgBuf': None, 'CreateTime': 1663310550, 
    'MsgSource': '<msgsource>\n\t<signature>v1_lgqBHNu/</signature>\n</msgsource>\n', 
    'PushContent': 'Timixi : suki', 'NewMsgId': 4254468380230777147, 
    'ActionUserName': '', 'ActionNickName': 'Timixi'
}

群聊消息
{
    'MsgId': 1753462794, 'FromUserName': '17883757265@chatroom', 
    'ToUserName': 'wxid_sfxvc2xx54rl12', 'MsgType': 1, 
    'Content': '花一个下午打牌', 'Status': 3, 'ImgStatus': 1, 
    'ImgBuf': None, 'CreateTime': 1663311817, 
    'MsgSource': '<msgsource>\n\t<alnode>\n\t\t<fr>1</fr>\n\t</alnode>\n\t<silence>0</silence>\n\t<membercount>5</membercount>\n\t<signature>v1_Z4jNcfXL</signature>\n</msgsource>\n', 
    'PushContent': '春日野熊 : 花一个下午打牌', 'NewMsgId': 1265081570314936894, 
    'ActionUserName': 'wxid_e5juxaghta4u21', 'ActionNickName': '春日野熊'
}
'''

class Plugin(StandardPlugin):
    def judgeTrigger(msg:str, data:Any) -> bool:
        return msg == "Suki" 
    def executeEvent(msg:str, data:Any, runtime:Runtime) -> Union[None, str]:
        #Send.sendMsg(f"{data['FromUserName']}","DaiSuki")
        runtime.msgQueue.sendMsg(f"{data['FromUserName']}","DaiSuki")
        return "OK"

'''
! Send类是危险的，频繁请求可能会导致风控，runtime中的msgQueue类是对Send类的再封装，对请求间隔时间进行了控制，建议使用

runtime.msgQueue.sendImage(ToUserName, ImagePath) 发送图片,图片地址可以为url和本地地址
runtime.msgQueue.sendMsg(ToUserName, Content, AtUsers="") 发送消息,暂时不支持@功能,建议将AtUsers项留空
runtime.msgQueue.sendAppMsg(ToUserName, Content) 发送App消息,可以发送小程序链接
runtime.msgQueue.sendVoice(ToUserName, VoicePath) 发送语音消息,注意微信语音消息为silk格式
runtime.msgQueue.sendEmoji(ToUserName, EmojiMd5, EmojiLen) 发送MD5表情
runtime.msgQueue.sendCdnImage(ToUserName, XmlStr) 发送CDN图片
runtime.msgQueue.sendVideo(ToUserName, VideoXml) 发送小视频

utils.basicEvents中的Send类封装了发送各类消息的方法
Send.sendImage(ToUserName, ImagePath) 发送图片,图片地址可以为url和本地地址
Send.sendMsg(ToUserName, Content, AtUsers="") 发送消息,暂时不支持@功能,建议将AtUsers项留空
Send.sendAppMsg(ToUserName, Content) 发送App消息,可以发送小程序链接
Send.sendVoice(ToUserName, VoicePath) 发送语音消息,注意微信语音消息为silk格式
Send.sendEmoji(ToUserName, EmojiMd5, EmojiLen) 发送MD5表情
Send.sendCdnImage(ToUserName, XmlStr) 发送CDN图片
Send.sendVideo(ToUserName, VideoXml) 发送小视频
'''

'''
若需要存储数据，请在/data/pluginData目录下新建与插件同名的文件夹，将文件存储在该文件夹下
例如要发送 /data/pluginData/template/tmp.png图片，则使用方法
runtime.msgQueue.sendImage(ToUserName, '/data/pluginData/template/tmp.png') 
'''

"""
若要添加定时任务，请使用threading模块的Timer组件
"""