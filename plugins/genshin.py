import requests
import httpx
import json
import random
import time
import hashlib
import os
from pathlib import Path
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import datetime
import string
from pathlib import Path
from typing import Union, Any
from utils.runtime import Runtime
from utils.standardPlugin import StandardPlugin

PLUGIN_INFO = {
    'name' : '原神查询',
    'version' : '0.0.1',
    'description' : '原神cookie绑定 [/gs bind] + [cookie]\n原神日常查询 [/gs note]\n发送 [/gs help] 获取绑定教程',
    'author' : 'UNIkeEN',
    'type' : 3,
}

ICON_LIST= [
    "https://i0.hdslb.com/bfs/article/df60cab523f0bf05868d7bbfcd06ed1b909929d1.jpg@942w_942h_progressive.webp",
    "https://i0.hdslb.com/bfs/article/71e35ba17d50cab7651d44fa98015beef00f3449.jpg@942w_942h_progressive.webp",
    "https://i0.hdslb.com/bfs/article/4255ee117624c0bf7a6228ec4d6afc85b8809852.jpg@942w_942h_progressive.webp",
    "https://i0.hdslb.com/bfs/article/434fe59e3b4c4e23874609ff58890c304c30f5aa.jpg@942w_942h_progressive.webp",
    "https://i0.hdslb.com/bfs/article/f792661790e18eeeb7a77ea01e890515e8306ea8.jpg@942w_942h_progressive.webp",
    "https://i0.hdslb.com/bfs/article/ef94d618faf948f4e21da1b7ff002e4ad319d189.jpg@942w_942h_progressive.webp",
    "https://i0.hdslb.com/bfs/article/89012b9294e0a574695f6ca4842b7018c7183b65.jpg@942w_942h_progressive.webp",
    "https://i0.hdslb.com/bfs/article/f76076c3f5d12c8750f1fea77fab56f8d37d56ec.jpg@942w_942h_progressive.webp",
    "https://i0.hdslb.com/bfs/article/5d3ac42abf0be1f438de0faf1a21141e4a7b6a75.jpg@777w_777h_progressive.webp",
    "https://i0.hdslb.com/bfs/article/10f26035e5e40456a2b59836e5cf2113dcdf4699.jpg@942w_942h_progressive.webp",
    "https://i0.hdslb.com/bfs/article/c19237f3809165d9375e6c9c7462cbafa416bcf0.jpg@942w_942h_progressive.webp"
]

SAVE_TMP_PATH = 'data/pluginData/genshin'

IMAGES_PATH = 'data/pluginData/genshin/images/'

FONTS_PATH = 'resources/fonts'
font_syht_m = ImageFont.truetype(os.path.join(FONTS_PATH, 'SourceHanSansCN-Normal.otf'), 18)
font_hywh_85w_ms = ImageFont.truetype(os.path.join(FONTS_PATH, '汉仪文黑.ttf'), 26)
font_hywh_85w = ImageFont.truetype(os.path.join(FONTS_PATH, '汉仪文黑.ttf'), 40)
font_sg_emj = ImageFont.truetype(os.path.join(FONTS_PATH, 'seguiemj.ttf'), 40)

class Plugin(StandardPlugin):
    def judgeTrigger(msg:str, data:Any) -> bool:
        return True
    def executeEvent(msg:str, data:Any, runtime:Runtime) -> Union[None, str]:
        if msg == '/gs help':
            runtime.msgQueue.sendMsg(f"{data['FromUserName']}", "绑定教程：https://docs.qq.com/doc/DTW9qQUhLaWNMZmRz")
        if GenshinDailyNote.judgeTrigger(msg, data):
            GenshinDailyNote.executeEvent(msg, data, runtime)
        if GenshinCookieBind.judgeTrigger(msg, data):
            GenshinCookieBind.executeEvent(msg, data, runtime)
        return "OK"

class GenshinDailyNote(StandardPlugin): 
    def judgeTrigger(msg:str, data:Any) -> bool:
        return msg == '/gs note'
    def executeEvent(msg:str, data:Any, runtime:Runtime) -> Union[None, str]:
        if data['FromUserName'][-9:] == '@chatroom':
            name = data['ActionUserName']
        else:
            name = data['FromUserName'] 
        ret = get_YSdailynote(name)
        if startswith_in(ret, ['查询失败']):
            runtime.msgQueue.sendMsg(f"{data['FromUserName']}", ret)
        else:
            runtime.msgQueue.sendImage(f"{data['FromUserName']}", ret)
        return "OK"


class GenshinCookieBind(StandardPlugin): 
    def judgeTrigger(msg:str, data:Any) -> bool:
        return startswith_in(msg, ['/gs bind '])
    def executeEvent(msg:str, data:Any, runtime:Runtime) -> Union[None, str]:
        msg_split=msg.split()
        uid=msg_split[2]
        msg=msg.replace('/gs','',1).strip()
        msg=msg.replace('bind','',1)
        msg=msg.replace(uid,'',1)
        if data['FromUserName'][-9:] == '@chatroom':
            name = data['ActionUserName']
        else:
            name = data['FromUserName'] 
        edit_bind_uid(name, uid, msg.strip())
        extra = "\n在群聊中绑定，请您务必将cookie等敏感信息撤回" if data['FromUserName'][-9:] == '@chatroom' else ""
        runtime.msgQueue.sendMsg(f"{data['FromUserName']}", "绑定成功" + extra)
        return "OK"

FAIL_REASON_1="请私聊使用/gs bind绑定uid和cookie\n绑定教程：https://docs.qq.com/doc/DTW9qQUhLaWNMZmRz?&u=792c5c9aa8164d73b27d7784a37709ce"
FAIL_REASON_2="可能原因：cookie过期或错误/查询次数到达今日上限，请重试或重新绑定！"

def md5(text: str) -> str:
    md5 = hashlib.md5()
    md5.update(text.encode())
    return md5.hexdigest()

# 米游社headers的ds_token，对应版本2.11.1
def get_ds(q="", b=None) -> str:
    if b:
        br = json.dumps(b)
    else:
        br = ""
    s = "xV8v4Qu54lUKrEYFZkJhB8cuOh9Asafs"
    t = str(int(time.time()))
    r = str(random.randint(100000, 200000))
    c = md5("salt=" + s + "&t=" + t + "&r=" + r + "&b=" + br + "&q=" + q)
    return f"{t},{r},{c}"

def get_headers(cookie, q='', b=None):
    headers = {
        'DS':                get_ds(q, b),
        'Origin':            'https://webstatic.mihoyo.com',
        'Cookie':            cookie,
        'x-rpc-app_version': "2.11.1",
        'User-Agent':        'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS '
                             'X) AppleWebKit/605.1.15 (KHTML, like Gecko) miHoYoBBS/2.11.1',
        'x-rpc-client_type': '5',
        'Referer':           'https://webstatic.mihoyo.com/'
    }
    return headers

def get_YSdailynote(qq_id):
    qq_id=str(qq_id)
    data_path=(f'data/pluginData/genshin/genshin.json')
    if not Path(data_path).is_file():
        Path(data_path).write_text(r'{}')
    with open(data_path, "r") as f:
        gs_base = json.load(f)
    if qq_id not in gs_base:
        return (f"查询失败\n{FAIL_REASON_1}")
    uid=gs_base[qq_id]['uid']
    cookie=gs_base[qq_id]['cookie']
    # print(uid)
    # print(cookie)
    server_id = "cn_qd01" if uid[0] == '5' else "cn_gf01"
    url = "https://api-takumi-record.mihoyo.com/game_record/app/genshin/api/dailyNote"
    headers = get_headers(q=f'role_id={uid}&server={server_id}', cookie=cookie)
    params = {
        "server":  server_id,
        "role_id": uid
    }
    #resp = requests.get(url=url, headers=headers, params=params)
    resp= httpx.get(url=url, headers=headers, params=params)
    data = resp.json()
    if data['retcode']!=0:
        return (f"查询失败\n{FAIL_REASON_2}")
    else:
        width=920
        height=720+(160 if data['data']['current_expedition_num']!=0 else 0)
        img = Image.new('RGBA', (width, height), (170,131,252,255))
        draw = ImageDraw.Draw(img)
        draw.rectangle((0, 120, width, height), fill=(255, 255, 255, 255))
        draw.text((width-420,40), "原神·实时便笺", fill=(255,255,255,255), font=font_hywh_85w)
        draw.text((width-120,44), "LITTLE\nUNIkeEN", fill=(255,255,255,255), font=font_syht_m)

        # 获取头像
        url_avatar = requests.get(random.choice(ICON_LIST))
        img_avatar = Image.open(BytesIO(url_avatar.content)).resize((150,150))
        mask = Image.new('RGBA', (150, 150), color=(0,0,0,0))
        # 圆形蒙版
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.ellipse((0,0, 150, 150), fill=(159,159,160))
        img.paste(img_avatar, (60, 80), mask)

        draw.text((250, 150), "uid："+str(uid), fill=(0, 0, 0, 255), font=font_hywh_85w)
        # 树脂
        draw.text((60, 280), f"原粹树脂：{data['data']['current_resin']}/{data['data']['max_resin']}", fill=(0, 0, 0, 255), font=font_hywh_85w)
        if data['data']['current_resin'] == 160:
            draw.text((520, 280), f"树脂已满", fill=(175, 175, 175, 255), font=font_hywh_85w)
        else:
            recover_time = datetime.datetime.now() + datetime.timedelta(seconds=int(data['data']['resin_recovery_time']))
            recover_time_day = '今天' if recover_time.day == datetime.datetime.now().day else '明天'
            draw.text((520, 280), f'将于{recover_time_day}{recover_time.strftime("%H:%M")}回满', fill=(175, 175, 175, 255), font=font_hywh_85w)
        # 宝钱
        draw.text((60, 360), f"洞天财瓮：{data['data']['current_home_coin']}/{data['data']['max_home_coin']}", fill=(0, 0, 0, 255), font=font_hywh_85w)
        if data['data']['current_home_coin'] == data['data']['max_home_coin']:
            draw.text((520, 360), f"洞天宝钱已满", fill=(175, 175, 175, 255), font=font_hywh_85w)
        else:
            recover_time = datetime.datetime.now() + datetime.timedelta(seconds=int(data['data']['home_coin_recovery_time']))
            d = int(data['data']['home_coin_recovery_time']) // 86400
            if d==0:
                draw.text((520, 360), f'将于今天{recover_time.strftime("%H:%M")}回满', fill=(175, 175, 175, 255), font=font_hywh_85w)
            elif d==1:
                draw.text((520, 360), f'将于明天{recover_time.strftime("%H:%M")}回满', fill=(175, 175, 175, 255), font=font_hywh_85w)
            elif d==2:
                draw.text((520, 360), f'将于后天{recover_time.strftime("%H:%M")}回满', fill=(175, 175, 175, 255), font=font_hywh_85w)
            else:
                draw.text((520, 360), f'将于{d}天后回满', fill=(175, 175, 175, 255), font=font_hywh_85w)
        # 委托
        draw.text((60, 440), f"已完成每日委托：{data['data']['finished_task_num']}/{data['data']['total_task_num']}", fill=(0, 0, 0, 255), font=font_hywh_85w)
        # 周本
        draw.text((60, 520), f"剩余周本消耗减半次数：{data['data']['remain_resin_discount_num']}/{data['data']['resin_discount_num_limit']}", fill=(0, 0, 0, 255), font=font_hywh_85w)
        # 探索派遣
        draw.text((60, 600), f"探索派遣：{data['data']['current_expedition_num']}/{data['data']['max_expedition_num']}", fill=(0, 0, 0, 255), font=font_hywh_85w)
        i=0
        for record in data['data']['expeditions']:
            url_role_avatar = requests.get(record['avatar_side_icon'])
            img_role_avatar = Image.open(BytesIO(url_role_avatar.content)).resize((90,90))
            if record['status']=="Finished":
                img_tmp=Image.open(IMAGES_PATH+'circle_green.png')
                img.paste(img_tmp, (60+i*177, 680))
                draw.text((60+i*177,790),"已完成",fill=(175,175,175,255),font=font_hywh_85w_ms)
            else:
                img_tmp=Image.open(IMAGES_PATH+'circle_grey.png')
                img.paste(img_tmp, (60+i*177, 680))
                h=int(record['remained_time']) // 3600
                m=int(record['remained_time']) % 3600 // 60
                draw.text((60+i*177-int(bool(h))*30,790),f"余{'' if h==0 else str(h)}时{m}分",fill=(0,0,0,255),font=font_hywh_85w_ms)
            img.alpha_composite(img_role_avatar, (60+i*177, 670))
            i+=1

        save_path=(f'{SAVE_TMP_PATH}/{qq_id}_genshin.png')
        img.save(save_path)
        return save_path

def edit_bind_uid(qq_id, uid, cookie):
    qq_id=str(qq_id)
    data_path=(f'data/pluginData/genshin/genshin.json')
    if not Path(data_path).is_file():
        Path(data_path).write_text(r'{}')
    with open(data_path, "r") as f:
        genshin_base = json.load(f)
    genshin_base[qq_id]={'uid':uid, 'cookie':cookie}
    with open(data_path, 'w') as f2:
        json.dump(genshin_base, f2, indent=4)
    return

def startswith_in(msg, checklist):
    for i in checklist:
        if msg.startswith(i):
            return True
    return False