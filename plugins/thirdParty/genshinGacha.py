from utils.basicEvent import *
from utils.basicConfigs import *
from utils.functionConfigs import *
from utils.standardPlugin import StandardPlugin
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import base64
import random
import re
from io import BytesIO
from pathlib import Path
from typing import List, Union, Any

from PIL import Image, ImageDraw, ImageFont

from plugins.thirdParty._genshinGacha.database import *
from plugins.thirdParty._genshinGacha.model import UserInfo, CardPoolProbability, CardPoolItem


digitalConversionDict = {
    "一": 1,
    "二": 2,
    "两": 2,
    "三": 3,
    "四": 4,
    "五": 5,
    "六": 6,
    "七": 7,
    "八": 8,
    "九": 9,
    "十": 10,
    "1": 1,
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "10": 10,
}

poolConversion = {
    '常驻': 'ordinary',
    '普通': 'ordinary',
    '普': 'ordinary',
    '常驻': 'ordinary',
    '角色': 'roleUp',
    '人物': 'roleUp',
    '武器': 'armUp',
}

curFileDir = Path(__file__).absolute().parent
fnt = ImageFont.truetype(str(curFileDir / '_genshinGacha' / 'config' / '惊鸿手书.ttf'), 35)

class GenshinGacha(): #移植自https://github.com/opq-osc/OPQ-SetuBot
    conversion_dict = {4: 'fourStar', 5: 'fiveStar'}

    def __init__(self,group_id: int, user_id: int, cardPool: str, cardCount: int):
        self.group_id = group_id
        self.user_id = user_id
        self.cardCount = cardCount
        self.cardPool = cardPool
        self.userConf: UserInfo = getUserConfig(user_id, cardPool)  # 用户信息
        self.cardPoolProbability: CardPoolProbability = getPoolProbabilityConfig(cardPool)  # 卡池的概率
        self.cardPoolItem: CardPoolItem = getPoolItemConfig(cardPool)  # 卡池中的物品

    def get_item_starLevel(self) -> int:
        """
        :return: 物品的星级,有保底
        """
        self.userConf.fiveStar.notGetCorrespondingCount += 1
        if self.userConf.fiveStar.notGetCorrespondingCount >= self.cardPoolProbability.floorCount.fiveStar:
            self.userConf.fiveStar.notGetCorrespondingCount = 0
            return 5
        self.userConf.fourStar.notGetCorrespondingCount += 1
        if self.userConf.fourStar.notGetCorrespondingCount >= self.cardPoolProbability.floorCount.fourStar:
            self.userConf.fourStar.notGetCorrespondingCount = 0
            return 4
        starLevel = random.choices(
            [5, 4, 3],
            [self.cardPoolProbability.item.fiveStarProbability,
             self.cardPoolProbability.item.fourStarProbability,
             100 - (self.cardPoolProbability.item.fiveStarProbability
                    + self.cardPoolProbability.item.fourStarProbability)]
        )[0]  # 物品星级
        if starLevel == 4:
            self.userConf.fourStar.notGetCorrespondingCount = 0
        elif starLevel == 5:
            self.userConf.fiveStar.notGetCorrespondingCount = 0
        return starLevel

    def extraction_arm_or_role(self, starLevel: int) -> dict:
        """
        根据概率选择武器还是人物
        :param starLevel: 星级
        :return: {'starLevel': 3, 'item': 'role'}
        """
        if starLevel == 3:
            return {'starLevel': 3, 'item': 'role'}

        return random.choices(
            [{'starLevel': starLevel, 'item': 'arm'}, {'starLevel': starLevel, 'item': 'role'}],
            [
                self.cardPoolProbability.arm.dict()[self.conversion_dict[starLevel]]['BaseProbability'],
                self.cardPoolProbability.role.dict()[self.conversion_dict[starLevel]]['BaseProbability']
            ]
        )[0]

    def iffloor(self, item: dict) -> Union[str, None]:
        """
        UP池的保底,up池歪了的话下一次必定是up物品
        :return:
        """
        if self.userConf.dict()[self.conversion_dict[item['starLevel']]]['certainUp']:
            changed_dict = self.userConf.dict()
            changed_dict[self.conversion_dict[item['starLevel']]]['certainUp'] = False  # 复位
            self.userConf = UserInfo(**changed_dict)
            # print('必定UP')
            return random.choice(self.cardPoolItem.dict()[self.conversion_dict[item['starLevel']]]['up'])
        # print('非保底UP')
        return None

    def extraction_specific_items(self, item: dict) -> str:
        """
        根据武器或角色的星级按照概率选择具体物品
        """
        if item['starLevel'] == 3:
            return random.choice(self.cardPoolItem.threeStar)
        if floorItem := self.iffloor(item):
            return floorItem
        specific_item = random.choices(
            [
                random.choice(self.cardPoolItem.dict()[self.conversion_dict[item['starLevel']]]['permanent']),
                random.choice(self.cardPoolItem.dict()[self.conversion_dict[item['starLevel']]]['up'] or ['占位'])
            ],
            [
                100 - self.cardPoolProbability.dict()[item['item']][self.conversion_dict[item['starLevel']]][
                    'UpProbability'],
                self.cardPoolProbability.dict()[item['item']][self.conversion_dict[item['starLevel']]]['UpProbability']
            ]
        )[0]
        if self.cardPool != 'ordinary' and (
                specific_item not in self.cardPoolItem.dict()[self.conversion_dict[item['starLevel']]]['up']):
            # print('非Up')
            changed_dict = self.userConf.dict()
            changed_dict[self.conversion_dict[item['starLevel']]]['certainUp'] = True  # 在up池出了非UP
            self.userConf = UserInfo(**changed_dict)
        return specific_item

    def draw(self, specific_item: list): #画出来有点丑要再优化
        """
        画图 
        :return:
        """
        #print([curFileDir / '_genshinGacha' / 'icon' / '{}.png'.format(name) for name in specific_item])
        pic = iter([curFileDir / '_genshinGacha' / 'icon' / '{}.png'.format(name) for name in specific_item])
        img_x = 130
        img_y = 160
        
        interval_x = 50  # x间距
        interval_y = 50  # y间距
        bg_x = 5 * img_x + 6 * interval_x  # 背景x
        bg_y = 2 * img_y + 3 * interval_y  # 背景y
        background = Image.new('RGB', (bg_x, bg_y), (39, 39, 54))
        x1 = 50  # 图像初始x坐标
        y1 = 50  # 图像初始y坐标
        if self.cardCount > 5:
            num_1 = 5
        else:
            num_1 = self.cardCount
        for i in range(num_1):
            background.paste(Image.open(next(pic)).resize((img_x, img_y), Image.ANTIALIAS), (x1, y1))
            x1 += (img_x + interval_x)
        x1 = 50  # 图像初始x坐标
        if self.cardCount - num_1 > 0:
            for i in range(self.cardCount - num_1):
                background.paste(Image.open(next(pic)).resize((img_x, img_y), Image.ANTIALIAS),
                                 (x1, img_y + 2 * interval_y))
                x1 += (img_x + interval_x)
        #print('done 3')
        save_path=(f'{SAVE_TMP_PATH}/{self.group_id}_genshingacha.png')
        background.save(save_path)
        
        return save_path   

    def main(self):
        """
        main
        :return:
        """
        if None in [self.userConf, self.cardPoolProbability, self.cardPoolItem]:
            #print('return 1')
            return
        cards_itemStarLevel: List[int] = [self.get_item_starLevel() for _ in range(self.cardCount)]  # 确定抽的卡都是什么星级的物品
        items: List[dict] = [self.extraction_arm_or_role(itemStarLevel) for itemStarLevel in cards_itemStarLevel]
        specific_item = [self.extraction_specific_items(item) for item in items]
        updateUserConfig(self.user_id, cardPool=self.cardPool, config=self.userConf)    
        print(specific_item)
        return self.draw(specific_item)

def match(msg):
    matchObj = re.fullmatch(r'原神(.*?)池(.*)连', msg)
    if matchObj:
        return True
    return False

class GenshinGachaPlugin(StandardPlugin):
    def judgeTrigger(msg:str, data:Any) -> bool:
        return match(msg)
    def executeEvent(msg:str, data:Any) -> Union[None, str]:
        if not check_config(data['group_id'],'Insider'):
            send(data['group_id'], TXT_PERMISSION_DENIED) #这里可能要改一下
        else:
            try:
                result = re.findall(r'原神(.*?)池(.*)连', msg)
                #print(result[0][1]+'    '+result[0][0])
                cardCount = digitalConversionDict[result[0][1]]
                cardPool = poolConversion[result[0][0]]
                #print(str(cardCount)+' '+cardPool)
                if cardCount:
                    if cardPool:
                        cls = GenshinGacha(data['group_id'], data['user_id'], cardPool, cardCount)
                        ret = cls.main()
                        if ret[-3:]=='png':
                            pic_path=(f'file:///{ROOT_PATH}/'+ret)
                            send(data['group_id'], f'[CQ:image,file={pic_path}]')
                    else:
                        send(data['group_id'], '好像没有这个池子呢')
                else:
                    send(data['group_id'], '只支持1-10连哦')
            except:
                pass
        return "OK"