import json
import os
from PIL import Image, ImageDraw, ImageFont
from typing import Union, Any
from utils.runtime import Runtime
from utils.standardPlugin import StandardPlugin

PLUGIN_INFO = {
    'name' : '帮助',
    'version' : '0.0.1',
    'description' : '/help',
    'author' : 'UNIkeEN',
    'type' : 1,
}

class Plugin(StandardPlugin):
    def judgeTrigger(msg:str, data:Any) -> bool:
        return msg == '/help' 
    def executeEvent(msg:str, data:Any, runtime:Runtime) -> Union[None, str]:
        runtime.msgQueue.sendImage(f"{data['FromUserName']}", show_config_card(data['FromUserName']))
        return "OK"

def show_config_card(group_id):
    i=1
    data_path=(f'configs/ChatRoomConf/{group_id}/config.json')
    with open(data_path, "r") as f2:
        config_base = json.load(f2)
    height=450+75*len(config_base)
    width=980
    img = Image.new('RGBA', (width, height), (6,162,183,255))
    draw = ImageDraw.Draw(img)
    draw.rectangle((0, 120, width, height), fill=(255, 255, 255, 255))
    draw.text((120, 150), f"群号:{group_id[:-9]}", fill=(6,162,183,255), font=font_hywh_85w)
    draw.text((60, 230), "●", fill=(6,162,183,255), font=font_hywh_85w)
    draw.text((120, 230), f"群聊功能", fill=(6,162,183,255), font=font_hywh_85w)
 
    i+=2
    for cf_value in config_base.values():
        try:
            if cf_value['enabled']:

                draw.text((120, 70+i*80), cf_value['name'] ,fill=(0, 0, 0, 255), font=font_hywh_85w)
                draw.text((360, 70+i*80), f"Ver. {cf_value['version']}", fill=(0, 0, 0, 255), font=font_hywh_85w)
                draw.text((600, 70+i*80), f"By {cf_value['author']}", fill=(0, 0, 0, 255), font=font_hywh_85w)
                draw.text((60, 70+i*80), "√", fill=(0, 0, 0, 255), font=font_hywh_85w)
            else:
                draw.text((120, 70+i*80), cf_value['name'] ,fill=(185, 185, 185, 255), font=font_hywh_85w)
                draw.text((360, 70+i*80), f"Ver. {cf_value['version']}", fill=(185, 185, 185, 255), font=font_hywh_85w)
                draw.text((600, 70+i*80), f"By {cf_value['author']}", fill=(185, 185, 185, 255), font=font_hywh_85w)
            i+=1
        except:
            pass
    draw.text((width-300,40), "功能配置", fill=(255,255,255,255), font=font_hywh_85w)
    draw.text((width-120,44), "LITTLE\nUNIkeEN", fill=(255,255,255,255), font=font_syht_m)
    if not os.path.isdir(os.path.join(SAVE_TMP_PATH, 'help')):
        os.mkdir(os.path.join(SAVE_TMP_PATH, 'help'))
    save_path=(f'{SAVE_TMP_PATH}/help/{group_id}_config.png')
    img.save(save_path)
    return save_path

FONTS_PATH = 'resources/fonts'
SAVE_TMP_PATH = 'data/pluginData'
font_syht_m = ImageFont.truetype(os.path.join(FONTS_PATH, 'SourceHanSansCN-Normal.otf'), 18)
font_hywh_85w_ms = ImageFont.truetype(os.path.join(FONTS_PATH, '汉仪文黑.ttf'), 26)
font_hywh_85w = ImageFont.truetype(os.path.join(FONTS_PATH, '汉仪文黑.ttf'), 40)
font_sg_emj = ImageFont.truetype(os.path.join(FONTS_PATH, 'seguiemj.ttf'), 40)