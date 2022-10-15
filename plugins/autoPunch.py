from typing import Union, Any
from threading import Timer
from utils.runtime import Runtime
from utils.standardPlugin import StandardPlugin

PLUGIN_INFO = {
    'name' : '网实打卡',
    'version' : '0.0.1',
    'description' : '',
    'author' : 'ChrisWhite',
    'type' : 4,
}

class Plugin(StandardPlugin):
    def judgeTrigger(msg:str, data:Any) -> bool:
        return msg == '/punch' 
    def executeEvent(msg:str, data:Any, runtime:Runtime) -> Union[None, str]:
        return "OK"