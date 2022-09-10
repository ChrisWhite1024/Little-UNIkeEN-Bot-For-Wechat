from typing import Union, Any
from utils.basicEvent import *
from utils.functionConfigs import check_config
from utils.standardPlugin import StandardPlugin
from utils.basicConfigs import TXT_PERMISSION_DENIED

class FireworksFace(StandardPlugin):
    def judgeTrigger(msg:str, data:Any) -> bool:
        return msg in ['放个烟花','烟花']
    def executeEvent(msg:str, data:Any) -> Union[None, str]:
        if not check_config(data['group_id'],'SuperEmoji'):
            send(data['group_id'], TXT_PERMISSION_DENIED)
        else:
            send(data['group_id'], "[CQ:face,id=333,type=sticker]")
        return "OK"

class FirecrackersFace(StandardPlugin):
    def judgeTrigger(msg:str, data:Any) -> bool:
        return msg in ['点个鞭炮','鞭炮']
    def executeEvent(msg:str, data:Any) -> Union[None, str]:
        if not check_config(data['group_id'],'SuperEmoji'):
            send(data['group_id'],TXT_PERMISSION_DENIED)
        else:
            send(data['group_id'], "[CQ:face,id=137,type=sticker]")
        return "OK"

class BasketballFace(StandardPlugin):
    def judgeTrigger(msg:str, data:Any) -> bool:
        return msg in ['投个篮球','投篮']
    def executeEvent(msg:str, data:Any) -> Union[None, str]:
        if not check_config(data['group_id'],'SuperEmoji'):
            send(data['group_id'],TXT_PERMISSION_DENIED)
        else:
            send(data['group_id'], "[CQ:face,id=114,type=sticker]")
        return "OK"

class HotFace(StandardPlugin):
    def judgeTrigger(msg:str, data:Any) -> bool:
        return msg in ['热死了', '好热', '太热了']
    def executeEvent(msg:str, data:Any) -> Union[None, str]:
        if not check_config(data['group_id'],'SuperEmoji'):
            send(data['group_id'],TXT_PERMISSION_DENIED)
        else:
            send(data['group_id'], "[CQ:face,id=340,type=sticker]")
        return "OK"