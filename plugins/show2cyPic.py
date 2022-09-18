import requests
from typing import Union, Any
from utils.runtime import Runtime
from utils.standardPlugin import StandardPlugin

PLUGIN_INFO = {
    'name' : '来点图图',
    'version' : '0.0.1',
    'description' : '来点图图',
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