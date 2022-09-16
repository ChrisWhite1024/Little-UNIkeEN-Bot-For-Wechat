import requests
import json
import os

# 发送消息
class Send():
  
  __headers = {'Content-Type': 'application/json'}
  __timeout = 10
  __GLOBAL_CONF_PATH = 'config.json'

  # 莫名其妙逻辑就跑通了，未曾设想的道路
  try:
    with open(__GLOBAL_CONF_PATH, 'r') as f:
      globalConfig = json.load(f)
    __SERVER_IP = globalConfig['SERVER_IP']
    __SERVER_PORT = globalConfig['SERVER_PORT']
    __WXID = globalConfig['WXID']
  except:
    pass

  __typeTable ={
    "SendImage" : 1,
    "SendAppMsg" : 49,
    "SendMsg" : 1,
    "SendVoice" : -1,
    "SendEmoji" : -1,
    "SendCdnImage" : -1,
    "SendVideo" : -1,
    "DownloadVoice" : -1,
    "MagicCgi" : -1
  }

  __payLoad = {}
  
  # 构造请求
  @classmethod
  def sendPayload(self, FunctionName):
    if self.__typeTable[FunctionName] != -1:
      self.__payLoad["MsgType"] = self.__typeTable[FunctionName]
    url="http://{}:{}/v1/LuaApiCaller?funcname={}&timeout={}&wxid={}".format(self.__SERVER_IP, self.__SERVER_PORT, FunctionName, self.__timeout, self.__WXID)
    try:
      response = requests.request("POST", url, headers=self.__headers, data=json.dumps(self.__payLoad))
      if response.json() == None:
        print(f"[E] (basicEvents.py)Send：{FunctionName}非法，请检查参数正确性")
      else:
        # 这里要改
        print(f"[L] (basicEvents.py)Send：消息发送成功，方法{FunctionName}")      
    except Exception as e:
      print(f'[E] (basicEvents.py)Send：Requests库请求失败：{e}')
    self.__payLoad = {}

  # 发送图片
  @classmethod
  def sendImage(self, ToUserName, ImagePath): 
    self.__payLoad["ToUserName"] = ToUserName
    self.__payLoad["ImagePath" if os.path.isfile(ImagePath) else "ImageUrl"] = ImagePath
    self.sendPayload("SendImage")
  # 发送消息 有待添加@功能
  @classmethod
  def sendMsg(self, ToUserName, Content, AtUsers=""): 
    self.__payLoad["ToUserName"] = ToUserName
    self.__payLoad["Content"] = Content
    self.__payLoad["AtUsers"] = AtUsers
    self.sendPayload("SendMsg")
  # 发送App消息
  @classmethod
  def sendAppMsg(self, ToUserName, Content): 
    self.__payLoad["ToUserName"] = ToUserName
    self.__payLoad["Content"] = Content
    self.sendPayload("SendAppMsg")
  # 发送语音消息
  @classmethod
  def sendVoice(self, ToUserName, VoicePath): 
    self.__payLoad["ToUserName"] = ToUserName
    self.__payLoad["VoicePath" if os.path.isfile(VoicePath) else "VoiceUrl"] = VoicePath 
    self.sendPayload("SendVoice")
  # 发送MD5表情
  @classmethod
  def sendEmoji(self, ToUserName, EmojiMd5, EmojiLen): 
    self.__payLoad["ToUserName"] = ToUserName
    self.__payLoad["EmojiMd5"] = EmojiMd5
    self.__payLoad["EmojiLen"] = EmojiLen
    self.sendPayload("SendEmoji")
  # 发送CDN图片
  @classmethod
  def sendCdnImage(self, ToUserName, XmlStr): 
    self.__payLoad["ToUserName"] = ToUserName
    self.__payLoad["XmlStr"] = XmlStr
    self.sendPayload("SendCdnImage")
  # 发送视频
  @classmethod
  def sendVideo(self, ToUserName, VideoXml): 
    self.__payLoad["ToUserName"] = ToUserName
    self.__payLoad["VideoXml"] = VideoXml
    self.sendPayload("SendVideo")