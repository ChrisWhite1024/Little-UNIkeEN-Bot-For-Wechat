import re
import requests
import datetime
import random
from pathlib import Path
from typing import Union, Any
from threading import Timer
from utils.runtime import Runtime
from utils.standardPlugin import StandardPlugin
from utils.responseImage import *

PLUGIN_INFO = {
    'name' : '拍一拍',
    'version' : '0.0.1',
    'description' : '小白讨厌被拍 ( >﹏<。)',
    'author' : 'ChrisWhite',
    'type' : 3,
}

PAT_LIST = [
    "别...别拍我，最讨厌你了！",
    "什么啊..就算你拍我我也不会高兴的",
    "达咩～",
    "大丈夫？",
    "总之你是个大笨蛋啦！",
    "区区邪神，竟敢侵入吾之左臂？",
    "颤抖吧！渺小的凡人~",
    "三次元的你们不要太过分了",
    "颤抖吧，愚蠢的人类",
    "这么有空还不去刷题？",
    "还拍还拍，记住你了！",
    "人类总是重复同样的错误。",
    "还拍，今晚的Rank别让我看到你是零鸭蛋",
    "拍哪里呢~，CTF入门了吗，我不喜欢弱者",
    "好耶击掌。弟弟妹妹们新生赛加油~",
    "让我看看谁在摸鱼",
    "盯～新生赛就盯着你了"
]

class Plugin(StandardPlugin):
    def judgeTrigger(msg:str, data:Any) -> bool:
        return data.get('EventName', False) == "ON_EVENT_PAT_MSG" and data.get('PattedUserName', False) == 'wxid_sfxvc2xx54rl12'
    def executeEvent(msg:str, data:Any, runtime:Runtime) -> Union[None, str]:
        runtime.msgQueue.sendMsg(f"{data['FromUserName']}", random.choice(PAT_LIST))
        return "OK"
