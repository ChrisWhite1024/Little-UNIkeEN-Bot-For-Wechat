import requests
from typing import Union, Any
from utils.runtime import Runtime
from utils.standardPlugin import StandardPlugin
import urllib.parse

PLUGIN_INFO = {
    'name' : '来点图图',
    'version' : '0.0.2',
    'description' : '我超，二次元！\n你今天要 [来点图图] 吗',
    'author' : 'UNIkeEN',
    'type' : 3,
}

class Plugin(StandardPlugin):
    def judgeTrigger(msg:str, data:Any) -> bool:
        return msg == '来点图图'
    def executeEvent(msg:str, data:Any, runtime:Runtime) -> Union[None, str]:
        pic_url = requests.get(url='https://tenapi.cn/acg',params={'return': 'json'}).json()['imgurl']
        runtime.msgQueue.sendImage(f"{data['FromUserName']}", pic_url)
        return "OK"

# 字符以...开头
def startswith_in(msg, checklist):
    for i in checklist:
        if msg.startswith(i):
            return True
    return False