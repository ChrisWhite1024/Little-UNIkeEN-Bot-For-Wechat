from pathlib import Path
from typing import Union, Any
from utils.basicEvent import *
from utils.basicConfigs import *
from utils.functionConfigs import *
from utils.standardPlugin import StandardPlugin
import mysql.connector
import json
from pymysql.converters import escape_string
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

class SearchSjtuSqlAll(StandardPlugin): 
    def judgeTrigger(msg:str, data:Any) -> bool:
        return startswith_in(msg, ['-qall ']) and data['group_id']==743740311
    def executeEvent(msg:str, data:Any) -> Union[None, str]:
        msg=msg[6:]
        send(data['group_id'],search_sql_all(msg))
        return "OK"

class SearchSjtuSql(StandardPlugin): 
    def judgeTrigger(msg:str, data:Any) -> bool:
        return startswith_in(msg, ['-sqlr ']) and data['group_id']==743740311
    def executeEvent(msg:str, data:Any) -> Union[None, str]:
        msg=msg.replace('-sqlr ','',1)
        send(data['group_id'],search_sql(msg))
        return "OK"

class SearchSjtuSqlPIC(StandardPlugin): 
    def judgeTrigger(msg:str, data:Any) -> bool:
        return startswith_in(msg, ['-sqlrp ']) and data['group_id']==743740311
    def executeEvent(msg:str, data:Any) -> Union[None, str]:
        msg=msg.replace('-sqlrp ','',1)
        ret = search_sql_PIC(msg)
        if ret=='错误，无法连接至数据库':
            send(data['group_id'],ret)
        else:
            send(data['group_id'], f'[CQ:image,file=files:///{ROOT_PATH}/'+ret+',id=40000]')
        return "OK"

def search_sql(cmd):
    try:
        mydb = mysql.connector.connect(**sqlConfig)
    except:
        return '错误，无法连接至数据库'
    mycursor = mydb.cursor()
    mycursor.execute("USE sjtu_name")
    #cmd=escape_string(cmd)
    mycursor.execute(f"SELECT id, name, jaccount, birthday, organize, classNo, qq, phone, dorm FROM students where {cmd}")
    data = list(mycursor)
    res = ''
    for id, name, jaccount, birthday, organize, classNo, qq, phone, dorm in data[:10]:
        birthday = str(birthday).replace('00:00:00','',1)
        organize = organize.replace('\n',',',1)
        res+=(f'{id} | {name} | {jaccount} | {organize} | {classNo} | {birthday} | {qq} | {phone} | {dorm} \n\n')
    if len(data)>10: 
        res+=(f'在库记录共【{len(data)}】条，多余信息已折叠，请输入更精确条件以查询')
    else:
        res+=(f'在库记录共【{len(data)}】条')
    return res
def search_sql_all(cmd):
    try:
        mydb = mysql.connector.connect(**sqlConfig)
    except:
        return '错误，无法连接至数据库'
    mycursor = mydb.cursor()
    mycursor.execute("USE sjtu_name")
    #cmd=escape_string(cmd)
    mycursor.execute(f"SELECT id, name, jaccount, birthday, organize, classNo, qq, phone, dorm, idcard, address FROM students where {cmd}")
    data = list(mycursor)
    res = ''
    for id, name, jaccount, birthday, organize, classNo, qq, phone, dorm, idcard, address in data[:1]:
        birthday = str(birthday).replace('00:00:00','',1)
        organize = organize.replace('\n',',',1)
        res+=(f'id: {id}\nname: {name}\njac: {jaccount}\norg: {organize}\nclass: {classNo}\nbirth: {birthday}\nqq: {qq}\nphone: {phone}\ndorm: {dorm}\nidcard: {idcard}\naddr: {address}')
    return res

def search_sql_PIC(cmd):
    try:
        mydb = mysql.connector.connect(**sqlConfig)
    except:
        return '错误，无法连接至数据库'
    mycursor = mydb.cursor()
    mycursor.execute("USE sjtu_name")
    #cmd=escape_string(cmd)
    mycursor.execute(f"SELECT id, name, jaccount, birthday, organize, classNo, qq, phone, dorm FROM students where {cmd}")
    data = list(mycursor)
    width=760
    height=(len(data) if len(data)<=10 else 10)*160+150
    img = Image.new('RGBA', (width, height), (235, 235, 235, 255))
    draw = ImageDraw.Draw(img)
    txt_size = draw.textsize("📦", font_sg_emj)
    draw.text(((width-txt_size[0])/2, 40), "📦", fill=(85, 85, 85, 255), font = font_sg_emj)
    i=0
    for id, name, jaccount, birthday, organize, classNo, qq, phone, dorm in data[:10]:
        wnx, wny = 60, 100+i*160
        draw.rectangle((60, 100+i*160, width-60, 240+i*160), fill=(255, 255, 255, 255))
        i+=1
        birthday = str(birthday).replace('00:00:00','',1)
        organize = organize.replace('\n',',',1)
        txt_size = draw.textsize(f"{id} {name} ", font = font_syht_ml)
        draw.text((wnx+30,wny+15), f"{id} {name} ", fill=(0,0,0,255), font = font_syht_ml)
        draw.text((wnx+30+txt_size[0],wny+15), f"{jaccount} ", fill=(115,115,115,255), font = font_syht_ml)
        str_l2 = organize+' '+(classNo if classNo!=None else ' ')
        draw.text((wnx+30,wny+65), str_l2, fill=(155,155,155,255), font = font_syht_mm)
        str_l3 = f'{qq} | ' if str(qq)!='None' and str(qq)!='' else ''
        flag=False
        if str_l3 !='':
            # 获取QQ头像
            url_avatar = requests.get(f'http://q2.qlogo.cn/headimg_dl?dst_uin={qq}&spec=100')
            img_avatar = Image.open(BytesIO(url_avatar.content)).resize((25,25))
            mask = Image.new('RGBA', (25, 25), color=(0,0,0,0))
            mask_draw = ImageDraw.Draw(mask)
            mask_draw.ellipse((0,0, 25, 25), fill=(159,159,160))
            img.paste(img_avatar, (wnx+30,wny+100), mask)
            flag=True
        str_l3 += f'{birthday} | ' if birthday!='None' else ''
        str_l3 += f'{phone} | ' if phone!=None and str(phone)!='' else ''
        str_l3 += f'{dorm} | ' if dorm!=None else ''
        # print(str_l3+'@@')
        try:
            if str_l3[-4]=='|':
                str_l3 = str_l3[:-4]
            if str_l3[-2]=='|':
                str_l3 = str_l3[:-2]
        except:
            pass
        if str_l3.strip()=='':
            str_l3 = ' '
        draw.text((wnx+30+(38 if flag else 0),wny+100), str_l3, fill=(155,155,155,255), font = font_syht_mm)
    if len(data)>10: 
        draw.text((60, height-48),f'在库记录共【{len(data)}】条，多余信息已折叠，请输入更精确条件以查询',fill=(155,155,155,255), font = font_syht_m)
    else:
        draw.text((60, height-48),f'在库记录共【{len(data)}】条',fill=(155,155,155,255), font = font_syht_m)
    
    save_path=(f'{SAVE_TMP_PATH}/kaihe.png')
    img.save(save_path)
    return save_path