from datetime import datetime
from typing import Union, Any
from utils.basicEvent import *
from utils.basicConfigs import *
from utils.functionConfigs import check_config
from utils.standardPlugin import StandardPlugin
from utils.accountOperation import get_user_coins, get_user_transactions, update_user_coins
from PIL import Image, ImageDraw, ImageFont

# 开启祈愿server命令
#dotnet GenshinPray.dll --launch-profile Production --urls http://127.0.0.1:7890
#IMG_PATH='home/code/ChrisWhite'
PRAY_SERVER_PATH='home/ubuntu/code/ChrisWhite/PrayImg/'

class GenshinPray(StandardPlugin): # 十连
    def judgeTrigger(msg:str, data:Any) -> bool:
        return msg in ['原神十连','原神单抽']
    def executeEvent(msg:str, data:Any) -> Union[None, str]:
        if data['message_type']=='group' and not check_config(data['group_id'],'Insider'):
            send(data['group_id'],TXT_PERMISSION_DENIED)
        else:
            target = data['group_id'] if data['message_type']=='group' else data['user_id']
            flag = 'PrayTen' if msg=='原神十连' else 'PrayOne'
            pic_url = requests.get(url=f'http://127.0.0.1:7890/api/RolePray/{flag}', params={'memberCode': data['user_id']}, headers={'authorzation': 'chriswhite'}).json()['data']['imgPath']
            
            send(target, f'[CQ:image,file=files:///{PRAY_SERVER_PATH+pic_url}]', data['message_type'])
            #send(target, str(pic_url), data['message_type'])
        return "OK"