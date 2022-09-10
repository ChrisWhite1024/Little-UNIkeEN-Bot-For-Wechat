from typing import Union, Any
from utils.basicEvent import *
from utils.basicConfigs import *
from utils.functionConfigs import check_config, check_config_mode
from utils.standardPlugin import StandardPlugin
import json
import random

book_path = 'resources/corpus/answerbook.json'
with open(book_path, "r") as f:
    BOOK_DICT = json.load(f)

class ChatWithAnswerbook(StandardPlugin): # NLP对话插件
    def judgeTrigger(msg:str, data:Any) -> bool:
        return startswith_in(msg, ['小🦄，','小马，','小🦄,','小马,']) and check_config_mode(data['group_id'],'Auto_Answer')=='answerbook'
    def executeEvent(msg:str, data:Any) -> Union[None, str]: 
        if data['message_type']=='group' and not check_config(data['group_id'],'Auto_Answer'):
            send(data['group_id'],TXT_PERMISSION_DENIED)
        target = data['group_id'] if data['message_type']=='group' else data['user_id']
        msg_inp = msg[2:]
        ran = random.sample(BOOK_DICT.keys(),1)[0]
        text = f'[CQ:reply,id='+str(data['message_id'])+']'+BOOK_DICT[ran]["answer"]
        send(target, text, data['message_type'])
        return "OK"