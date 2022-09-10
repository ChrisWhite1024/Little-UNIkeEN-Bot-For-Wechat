from PIL import Image, ImageDraw, ImageFont
import os

ip='127.0.0.1'
port=5555

SERVER=f'ws://{ip}:{port}'
HEART_BEAT=5005
RECV_TXT_MSG=1
RECV_TXT_CITE_MSG=49
RECV_PIC_MSG=3
USER_LIST=5000
GET_USER_LIST_SUCCSESS=5001
GET_USER_LIST_FAIL=5002
TXT_MSG=555
PIC_MSG=500
AT_MSG=550
CHATROOM_MEMBER=5010
CHATROOM_MEMBER_NICK=5020
PERSONAL_INFO=6500
DEBUG_SWITCH=6000
PERSONAL_DETAIL=6550
DESTROY_ALL=9999
JOIN_ROOM=10000

#代理配置
proxies={
    "http":None,
    "https":None,
} 

TXT_PERMISSION_DENIED = ""

# 根路径与资源路径
ROOT_PATH = os.path.dirname(os.path.realpath(__file__))[:-6]
FONTS_PATH = 'resources/fonts'
IMAGES_PATH = 'resources/images/'
SAVE_TMP_PATH = 'data/tmp'

# 画图颜色常量与文字
BACK_CLR = {'r':(255, 232, 236, 255),'g':(219, 255, 228, 255),'h':(234, 234, 234, 255),'o':(254, 232, 199, 255)}
FONT_CLR = {'r':(221, 0, 38, 255),'g':(0, 191, 48, 255),'h':(64, 64, 64, 255),'o':(244, 149 ,4, 255)}
font_syht_m = ImageFont.truetype(os.path.join(FONTS_PATH, 'SourceHanSansCN-Normal.otf'), 18)
font_syht_mm = ImageFont.truetype(os.path.join(FONTS_PATH, 'SourceHanSansCN-Normal.otf'), 24)
font_syht_ml = ImageFont.truetype(os.path.join(FONTS_PATH, 'SourceHanSansCN-Normal.otf'), 32)
font_hywh_85w = ImageFont.truetype(os.path.join(FONTS_PATH, '汉仪文黑.ttf'), 40)
font_hywh_85w_xs = ImageFont.truetype(os.path.join(FONTS_PATH, '汉仪文黑.ttf'), 18)
font_hywh_85w_s = ImageFont.truetype(os.path.join(FONTS_PATH, '汉仪文黑.ttf'), 20)
font_hywh_85w_mms = ImageFont.truetype(os.path.join(FONTS_PATH, '汉仪文黑.ttf'), 25)
font_hywh_85w_ms = ImageFont.truetype(os.path.join(FONTS_PATH, '汉仪文黑.ttf'), 30)
font_hywh_85w_l = ImageFont.truetype(os.path.join(FONTS_PATH, '汉仪文黑.ttf'), 55)
font_sg_emj = ImageFont.truetype(os.path.join(FONTS_PATH, 'seguiemj.ttf'), 55)
font_sg_emj_l = ImageFont.truetype(os.path.join(FONTS_PATH, 'seguiemj.ttf'), 75)