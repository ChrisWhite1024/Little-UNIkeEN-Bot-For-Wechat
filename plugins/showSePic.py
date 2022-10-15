import requests
from typing import Union, Any
from utils.runtime import Runtime
from utils.standardPlugin import StandardPlugin
import urllib.parse

PLUGIN_INFO = {
    'name' : '来点涩涩',
    'version' : '0.0.1',
    'description' : '发送 [来点涩涩] + [关键词] 来康好康的\n顺带一提R18已经关闭，上课也能安心看哦（大嘘）',
    'author' : 'UNIkeEN',
    'type' : 2,
}

class Plugin(StandardPlugin):
    def judgeTrigger(msg:str, data:Any) -> bool:
        return startswith_in(msg, ['来点涩涩']) 
    def executeEvent(msg:str, data:Any, runtime:Runtime) -> Union[None, str]:
        msg_split = msg.split()
        if len(msg_split)==0:
            tag=''
        else:
            tag=msg.replace('来点涩涩','',1)
            tag=tag.strip().split()
            tagText = ""
            for t in tag:
                tagText += urllib.parse.quote(t) + '|'
            tagText = tagText[:-1]
            try:  
                pic_url = requests.get(url=f"https://api.lolicon.app/setu/v2?tag={tagText}&r18=0&size=regular",params={'return': 'json'}).json()['data'][0]['urls']['regular']
                runtime.msgQueue.sendImage(f"{data['FromUserName']}", pic_url)
            except:
                pass
        return "OK"

# 字符以...开头
def startswith_in(msg, checklist):
    for i in checklist:
        if msg.startswith(i):
            return True
    return False