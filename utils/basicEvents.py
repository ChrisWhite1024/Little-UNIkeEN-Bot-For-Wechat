import requests
import json
import os
from utils.basicConfigs import SERVER_IP, SERVER_PORT

HTTP_URL = f"http://{SERVER_IP}:{SERVER_PORT}/v1/"

# 发送消息
class Send():
  headers = {'Content-Type': 'application/json'}

  def __init__(self) -> None:
    self.timeout = 10
    self.wxid = "wxid_sfxvc2xx54rl12"
    self.typeTable ={"SendImage":1,"SendAppMsg":49,"SendMsg":1,"SendVoice":-1,"SendEmoji":-1,"SendCdnImage":-1,"SendVideo":-1,"DownloadVoice":-1,"MagicCgi":-1}
    self.payLoad = {}

  # 构造请求
  def sendPayload(self, FunctionName):
    if self.typeTable[FunctionName] != -1:
      self.payLoad["MsgType"] = self.typeTable[FunctionName]
    payload = json.dumps(self.payLoad)
    headers = {'Content-Type': 'application/json'}
    url="http://43.138.112.209:8081/v1/LuaApiCaller?funcname={}&timeout={}&wxid={}".format(FunctionName, self.timeout, self.wxid)
    try:
      response = requests.request("POST", url, headers=headers, data=payload)
      if response.json() == None:
        print(f"[E] (basicEvents.py)Send：{FunctionName}非法，请检查参数正确性")
      else:
        # 这里要改
        print(f"[L] (basicEvents.py)Send：消息发送成功，方法{FunctionName}")      
    except Exception as e:
      print(f'[E] (basicEvents.py)Send：Requests库请求失败：{e}')
    self.payLoad = {}

  # 发送图片
  def sendImage(self, ToUserName, ImagePath): 
    self.payLoad["ToUserName"] = ToUserName
    self.payLoad["ImagePath" if os.path.isfile(ImagePath) else "ImageUrl"] = ImagePath
    self.sendPayload("SendImage")
  # 发送消息 有待添加@功能
  def sendMsg(self, ToUserName, Content, AtUsers=""): 
    self.payLoad["ToUserName"] = ToUserName
    self.payLoad["Content"] = Content
    self.payLoad["AtUsers"] = AtUsers
    self.sendPayload("SendMsg")
  # 发送App消息
  def sendAppMsg(self, ToUserName, Content): 
    self.payLoad["ToUserName"] = ToUserName
    self.payLoad["Content"] = Content
    self.sendPayload("SendAppMsg")
  # 发送语音消息
  def sendVoice(self, ToUserName, VoicePath): 
    self.payLoad["ToUserName"] = ToUserName
    self.payLoad["VoicePath" if os.path.isfile(VoicePath) else "VoiceUrl"] = VoicePath 
    self.sendPayload("SendVoice")
  # 发送MD5表情
  def sendEmoji(self, ToUserName, EmojiMd5, EmojiLen): 
    self.payLoad["ToUserName"] = ToUserName
    self.payLoad["EmojiMd5"] = EmojiMd5
    self.payLoad["EmojiLen"] = EmojiLen
    self.sendPayload("SendEmoji")
  # 发送CDN图片
  def sendCdnImage(self, ToUserName, XmlStr): 
    self.payLoad["ToUserName"] = ToUserName
    self.payLoad["XmlStr"] = XmlStr
    self.sendPayload("SendCdnImage")
  # 发送视频
  def sendVideo(self, ToUserName, VideoXml): 
    self.payLoad["ToUserName"] = ToUserName
    self.payLoad["VideoXml"] = VideoXml
    self.sendPayload("SendVideo")