from typing import Union, Any
from utils.basicEvents import *
from utils.basicConfigs import *
from utils.standardPlugin import StandardPlugin

class HelloWorld(StandardPlugin):
    def judgeTrigger(msg:str, data:Any) -> bool:
        return msg == "hello"
    def executeEvent(msg:str, data:Any) -> Union[None, str]:
        x = Send()
        x.sendMsg("zhanshen9045","Hello World")
        return "OK"