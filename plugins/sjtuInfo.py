from PIL import Image, ImageDraw, ImageFont
import json
import httpx
from pathlib import Path
from io import BytesIO
from typing import Union, Any
from utils.basicEvent import *
from utils.basicConfigs import *
from utils.functionConfigs import check_config
from utils.standardPlugin import StandardPlugin

class ShowSjtuInfo(StandardPlugin):
    def judgeTrigger(msg:str, data:Any) -> bool:
        return startswith_in(msg, ['-sjtu '])
    def executeEvent(msg:str, data:Any) -> Union[None, str]:
        if data['message_type']=='group' and not check_config(data['group_id'],'Sjtu_Info'):
            send(data['group_id'],TXT_PERMISSION_DENIED)
            return "OK"
        else:
            msg_split=msg.split()
            target = data['group_id'] if data['message_type']=='group' else data['user_id']
            if msg_split[1] in ['lib', 'library', 'tsg']:
                send(target, f'[CQ:image,file=files:///{ROOT_PATH}/'+get_lib_info()+',id=40000]', data['message_type'])
            elif msg_split[1] in ['st','shitang', 'canteen','ct']:
                send(target, f'[CQ:image,file=files:///{ROOT_PATH}/'+get_canteen_info()+',id=40000]',data['message_type'])
            return "OK"

def get_lib_info():
    url = "https://zgrstj.lib.sjtu.edu.cn/cp"
    ret = httpx.get(url)
    data = json.loads(ret.text[12:-2])['numbers']
    width=720
    height=210+280*((len(data)+1)//2)
    img = Image.new('RGBA', (width, height), (46, 192, 189, 255))
    draw = ImageDraw.Draw(img)
    draw.rectangle((0, 120, width, height), fill=(255, 255, 255, 255))
    draw.text((width-340,40), "图书馆查询", fill=(255,255,255,255), font=font_hywh_85w)
    draw.text((width-120,44), "LITTLE\nUNIkeEN", fill=(255,255,255,255), font=font_syht_m)
    for i in range(len(data)):
        record = data[i]
        if record['max']!=0:
            percent = int(record['inCounter']/record['max']*100)
        else:
            percent=0
        clr='g'
        if percent>=60:
            clr='o'
        if percent>=80:
            clr='r'
        if record['inCounter']==0:
            clr='h'
        rec_width = 220
        rec_height = 180
        nw_x = 90+(i%2)*(width-180-rec_width)
        nw_y = 200+(i//2)*(rec_height+90)
        draw.rectangle((nw_x, nw_y, nw_x+rec_width, nw_y+rec_height), fill=BACK_CLR[clr])
        draw.text((nw_x+30,nw_y+30), record['areaName'],fill=FONT_CLR[clr], font=font_hywh_85w_s)
        draw.text((nw_x+30,nw_y+60), f"在馆人数 {record['inCounter']}/{record['max']}",fill=FONT_CLR[clr], font=font_hywh_85w_s)
        txt_per = (str(percent)+"%") if clr!="h" else "关闭"
        txt_size = draw.textsize(txt_per, font_hywh_85w_l) # 获取字符串在图片上长度的一种算法
        draw.text((nw_x+(rec_width-txt_size[0])/2,nw_y+90), txt_per, fill=FONT_CLR[clr], font=font_hywh_85w_l)

        draw.text((30,height-48),'* API借鉴自chshzhe/GuGuBot', fill=(175,175,175,255), font=font_syht_m)

    save_path=(f'{SAVE_TMP_PATH}/lib_info.png')
    img.save(save_path)
    return save_path

def get_canteen_info():
    ret = httpx.get('https://canteen.sjtu.edu.cn/CARD/Ajax/Place')
    data = ret.json()
    data.sort(key=lambda x: x['Id'])
    width=720
    height=210+280*((len(data)+1)//2)
    img = Image.new('RGBA', (width, height), (46, 192, 189, 255))
    draw = ImageDraw.Draw(img)
    draw.rectangle((0, 120, width, height), fill=(255, 255, 255, 255))
    draw.text((width-300,40), "餐厅查询", fill=(255,255,255,255), font=font_hywh_85w)
    draw.text((width-120,44), "LITTLE\nUNIkeEN", fill=(255,255,255,255), font=font_syht_m)
    for i in range(len(data)):
        record = data[i]
        if record['Seat_s']!=0:
            percent = int(record['Seat_u']/record['Seat_s']*100)
            clr='g'
            if percent>=60:
                clr='o'
            if percent>=80:
                clr='r'
        else:
            clr="h"
        rec_width = 220
        rec_height = 180
        nw_x = 90+(i%2)*(width-180-rec_width)
        nw_y = 200+(i//2)*(rec_height+90)
        draw.rectangle((nw_x, nw_y, nw_x+rec_width, nw_y+rec_height), fill=BACK_CLR[clr])
        draw.text((nw_x+30,nw_y+30), record['Name'],fill=FONT_CLR[clr], font=font_hywh_85w_s)
        draw.text((nw_x+30,nw_y+64), f"内有人数 {record['Seat_u']}/{record['Seat_s']}",fill=FONT_CLR[clr], font=font_hywh_85w_xs)
        txt_per = (str(percent)+"%") if clr!="h" else "关闭"
        txt_size = draw.textsize(txt_per, font_hywh_85w_l)
        draw.text((nw_x+(rec_width-txt_size[0])/2,nw_y+90), txt_per, fill=FONT_CLR[clr], font=font_hywh_85w_l)

        draw.text((30,height-48),'* API借鉴自chshzhe/GuGuBot', fill=(175,175,175,255), font=font_syht_m)

    save_path=(f'{SAVE_TMP_PATH}/st_info.png')
    img.save(save_path)
    return save_path