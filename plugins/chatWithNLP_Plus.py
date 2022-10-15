from typing import Union, Any
from utils.runtime import Runtime
from utils.standardPlugin import StandardPlugin
import random
import requests

class ChatBot_of_Baidu(object):
    def __init__(self) -> None:
        self.access_token = '24.6eec6264da66861af4c43941c8d666f2.2592000.1668274912.282335-27898116'
        self.url = url = 'https://aip.baidubce.com/rpc/2.0/unit/bot/chat?access_token=' + self.access_token
        self.post_data_0 = "{\"bot_session\":\"\",\"log_id\":\"7758521\",\"request\":{\"bernard_level\":1,\"client_session\":\"{\\\"client_results\\\":\\\"\\\", \\\"candidate_options\\\":[]}\",\"query\":"
        self.post_data_1 = ",\"query_info\":{\"asr_candidates\":[],\"source\":\"KEYBOARD\",\"type\":\"TEXT\"},\"updates\":\"\",\"user_id\":\"88888\"},\"bot_id\":\"1247719\",\"version\":\"2.0\"}"
        self.headers = {'content-type': 'application/x-www-form-urlencoded'}

    def Process(self, Text: str):
        response = requests.post(self.url,
                                 data=(self.post_data_0 + "\"" + Text + "\"" + self.post_data_1).encode("utf-8"),
                                 headers=self.headers)
        responseList = []
        if response:
            res = dict(response.json())
            for i in res['result']["response"]['action_list']:
                responseList.append(i['say'])
        return responseList

    def Send(self, Text: str):
        k_ = self.Process(Text)
        if len(k_) <= 0:
            return "竟无语凝噎"
        return k_[random.randint(0, len(k_) - 1)]

class Plugin(StandardPlugin): # NLP对话插件
    def judgeTrigger(msg:str, data:Any) -> bool:
        return startswith_in(msg, ['小白小白，','小白小白,'])
    def executeEvent(msg:str, data:Any, runtime:Runtime) -> Union[None, str]:
        BOT = ChatBot_of_Baidu()
        msg_inp = msg[5:]
        ret = BOT.Send(msg_inp)
        runtime.msgQueue.sendMsg(f"{data['FromUserName']}", ret)
        sleep(0.3)
        # if ret != "我好像不明白捏qwq":
        #     voice = send_genshin_voice(ret+'。')
        #     send(target, f'[CQ:record,file=files://{ROOT_PATH}/{voice}]', data['message_type'])
        return "OK"

def startswith_in(msg, checklist):
    for i in checklist:
        if msg.startswith(i):
            return True
    return False

PLUGIN_INFO = {
    'name' : 'NLP对话 PLUS',
    'version' : '0.0.1',
    'description' : '输入 [小白小白，] + [句子] 来和小白对话 \nHint:（Using Baidu API）',
    'author' : 'Andrew82106',
    'type' : 3,
}