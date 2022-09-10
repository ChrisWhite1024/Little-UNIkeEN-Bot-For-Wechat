from datetime import datetime
from typing import Union, Any
from utils.basicEvent import *
from utils.basicConfigs import *
from utils.functionConfigs import check_config
from utils.standardPlugin import StandardPlugin
from utils.accountOperation import get_user_coins, get_user_transactions, update_user_coins
from PIL import Image, ImageDraw, ImageFont

class CrazyPoke(StandardPlugin): # 查询近期交易记录
    def judgeTrigger(msg:str, data:Any) -> bool:
        return msg.startswith('戳')
    def executeEvent(msg:str, data:Any) -> Union[None, str]:
        if data['message_type']=='group' and not check_config(data['group_id'],'Insider'):
            send(data['group_id'],TXT_PERMISSION_DENIED)
        else:
            target = data['group_id'] if data['message_type']=='group' else data['user_id']
            #print(data['user_id'])
            msg_split = msg.split()
            #print(msg_split)
            if len(msg_split)==3 and msg_split[1][:6]=='[CQ:at':
                try:
                    aim_id=msg_split[1].replace('[CQ:at,qq=','',1)
                    aim_id=int(aim_id.replace(']','',1))
                    num_times=int(msg_split[2])
                except:
                    return "OK"
                assert (1<=num_times and num_times<=50)
                assert aim_id != BOT_SELF_QQ
                print(f"[CQ:poke,qq={aim_id}]")
                for i in range(num_times):
                    send(target, f"[CQ:poke,qq={aim_id}]", data['message_type'])
        return "OK"