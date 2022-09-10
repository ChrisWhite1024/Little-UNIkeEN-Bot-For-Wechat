from typing import Union, Any
from utils.basicEvent import send
from utils.functionConfigs import check_config
from utils.standardPlugin import StandardPlugin

class Chai_Jile(StandardPlugin):
    def judgeTrigger(msg:str, data:Any) -> bool:
        return ('我寄' in msg or '寄了' in msg) and (data['user_id']==1321711834)
    def executeEvent(msg:str, data:Any) -> Union[None, str]:
        send(data['group_id'], 'patpat柴[CQ:face,id=49], 不要伤心😘')
        return "OK"

class Yuan_Jile(StandardPlugin):
    def judgeTrigger(msg:str, data:Any) -> bool:
        #return ('ttt' in msg)
        return ('真弱' in msg or '寄了' in msg or '好菜' in msg) and (data['user_id']==1821035364) and (data['group_id']==1006366067)
    def executeEvent(msg:str, data:Any) -> Union[None, str]:
        send(data['group_id'], '😅😅😅😅😅😅😅😅😅😅')
        return "OK"