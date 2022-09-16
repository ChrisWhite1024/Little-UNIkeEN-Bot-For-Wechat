from typing import Union, Any
from utils.basicEvents import Send
from utils.standardPlugin import StandardPlugin

class HelloWorld(StandardPlugin):
    def judgeTrigger(msg:str, data:Any) -> bool:
        return msg == "hello"
    def executeEvent(msg:str, data:Any) -> Union[None, str]:
        Send.sendMsg(f"{data['FromUserName']}","Hello World")
        return "OK"


