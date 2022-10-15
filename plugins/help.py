import json
import os
import datetime
from PIL import Image, ImageDraw, ImageFont
from typing import Union, Any
from utils.runtime import Runtime
from utils.standardPlugin import StandardPlugin
from utils.responseImage import *

PLUGIN_INFO = {
    'name' : '插件查询',
    'version' : '0.2.1',
    'description' : '显示已装载插件的详细信息\n发送 [/help] 获取帮助',
    'author' : 'UNIkeEN',
    'type' : 3,
}

SAVE_TMP_PATH = 'data/pluginData/help'

class Plugin(StandardPlugin):
    def judgeTrigger(msg:str, data:Any) -> bool:
        return msg == '/help' 
    def executeEvent(msg:str, data:Any, runtime:Runtime) -> Union[None, str]:
        runtime.msgQueue.sendImage(f"{data['FromUserName']}", show_config_card(data['FromUserName'], runtime))
        return "OK"

def show_config_card(group_id: str, runtime: Runtime):
    today_str=str(datetime.date.today())
    if group_id[-9:] == '@chatroom':
        data_path=(f'configs/ChatRoomConf/{group_id}/config.json')
        group_id = group_id[:-9] 
        flag = 1
    else:
        data_path=(f'configs/UserConf/config.json')
        flag = 2
    img = ResponseImage(
        title = '聊天功能配置',
        footer = f'更新日期 {today_str}',
        primaryColor = PALETTE_SJTU_GREEN,
        layout = 'two-column')
    img.addCard(
        ResponseImage.RichContentCard(
            raw_content=[
                ('title', f"对话ID"),
                ('separator',),
                ('subtitle', f"{group_id}")
            ]
        )
    )
    with open(data_path, "r") as f2:
        config_base = json.load(f2)
    for key in config_base.keys():
        if flag == 1:
            desc = runtime.preLoader.CHATROOM_MODULE_LIST[key].PLUGIN_INFO['description']
        elif flag == 2: 
            desc = runtime.preLoader.USER_MODULE_LIST[key].PLUGIN_INFO['description']
        cf_value = config_base[key]
        width = (len(cf_value['version']) + len(cf_value['author'])) / 2 + 3
        try:
            if cf_value['enabled']:
                img.addCard(
                    ResponseImage.RichContentCard(
                        raw_content=[
                            ('title', cf_value['name']),
                            ('separator',),
                            ('keyword', "{:<18}{:<18}".format("版本", "作者")),
                            ('subtitle', "{:<20}{:<20}".format(cf_value['version'], cf_value['author'])),
                            ('keyword', '描述'),
                            ('body', desc),
                        ]
                    )
                )
        except:
            pass
    save_path=(f'{SAVE_TMP_PATH}/{group_id}_config.png')
    img.generateImage(save_path)
    return save_path
