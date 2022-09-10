from typing import Union, Any
from utils.basicEvent import *
from utils.basicConfigs import *
from utils.functionConfigs import *
from utils.standardPlugin import StandardPlugin

class ShowHelp(StandardPlugin): 
    def judgeTrigger(msg:str, data:Any) -> bool:
        return startswith_in(msg,['-help'])
    def executeEvent(msg:str, data:Any) -> Union[None, str]:
        target = data['group_id'] if data['message_type']=='group' else data['user_id']
        flag_id = data['group_id'] if data['message_type']=='group' else 0
        send(target, f'[CQ:image,file=files:///{ROOT_PATH}/'+show_config_card(flag_id)+',id=40000]',data['message_type'])
        return "OK"

class ShowStatus(StandardPlugin): 
    def judgeTrigger(msg:str, data:Any) -> bool:
        return msg == '-test status' 
    def executeEvent(msg:str, data:Any) -> Union[None, str]:
        target = data['group_id'] if data['message_type']=='group' else data['user_id']
        send(target, 'status: online\n'+VERSION_TXT,data['message_type'])
        return "OK"