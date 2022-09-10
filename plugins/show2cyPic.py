from typing import Union, Any
import requests
import json
from utils.basicEvent import *
from utils.basicConfigs import *
from utils.functionConfigs import *
from utils.standardPlugin import StandardPlugin
import urllib.parse
class Show2cyPIC(StandardPlugin): 
    def judgeTrigger(msg:str, data:Any) -> bool:
        return msg == '来点图图'
    def executeEvent(msg:str, data:Any) -> Union[None, str]:
        if data['message_type']=='group' and not check_config(data['group_id'],'2cyPIC'):
                send(data['group_id'],TXT_PERMISSION_DENIED)
        else:  
            target = data['group_id'] if data['message_type']=='group' else data['user_id']
            pic_url = requests.get(url='https://tenapi.cn/acg',params={'return': 'json'}).json()['imgurl']
            send(target,'[CQ:image,file=' + pic_url + ']', data['message_type'])
        return "OK"

class ShowSePIC(StandardPlugin): 
    def judgeTrigger(msg:str, data:Any) -> bool:
        return startswith_in(msg, ['来点涩涩'])
    def executeEvent(msg:str, data:Any) -> Union[None, str]:
        if data['message_type']=='group' and (data['group_id'] not in [185667006,835765215]):
            send(data['group_id'],TXT_PERMISSION_DENIED)
        else:
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
                    target = data['group_id'] if data['message_type']=='group' else data['user_id']
                    send(target,'[CQ:image,file=' + pic_url + ',type=flash]',data['message_type'])
                except:
                    pass
        return "OK"