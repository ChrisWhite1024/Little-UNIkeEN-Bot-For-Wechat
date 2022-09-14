import requests
import json
from utils.basicConfigs import SERVER_IP, SERVER_PORT

HTTP_URL = f"http://{SERVER_IP}:{SERVER_PORT}/v1/"

headers = {
  'Content-Type': 'application/json'
}
# 发送消息

class Send():
  def __init__(self) -> None:
    self.timeout = 10
    self.wxid = "wxid_sfxvc2xx54rl12"
    self.typeTable ={"SendImage":1,"SendAppMsg":49,"SendMsg":1,"SendVoice":-1,"SendEmoji":-1,"SendCdnImage":-1,"SendVideo":-1,"DownloadVoice":-1,"MagicCgi":-1}
    self.payLoad = {}
  def sendPayload(self, FunctionName):
    if self.typeTable[FunctionName] != -1:
      self.payLoad["MsgType"] = self.typeTable[FunctionName]
    payload = json.dumps(self.payLoad)
    headers = {'Content-Type': 'application/json'}
    url="http://43.138.112.209:8081/v1/LuaApiCaller?funcname={}&timeout={}&wxid={}".format(FunctionName, self.timeout, self.wxid)
    try:
      response = requests.request("POST", url, headers=headers, data=payload)
    except Exception as e:
      print(e)
    self.payLoad = {}

  def sendImage(self, ToUserName, ImageUrl):
    if len(ImageUrl) <= 4:
      print("INFO: 传输的图片路径有误")
      return
    self.payLoad["ToUserName"] = ToUserName
    self.payLoad["ImageUrl" if "http" == ImageUrl[0:5] else "ImagePath"] = ImageUrl
    #后端生成图片的时候记住不能以http开头
    self.sendPayload("SendImage")

  def sendMsg(self, ToUserName, Content, AtUsers=""):
    self.payLoad["ToUserName"] = ToUserName
    self.payLoad["Content"] = Content
    self.payLoad["AtUsers"] = AtUsers
    self.sendPayload("SendMsg")

  def sendAppMsg(self, ToUserName, Content): 
    self.payLoad["ToUserName"] = ToUserName
    self.payLoad["Content"] = Content
    self.sendPayload("SendAppMsg")

  def sendVoice(self, ToUserName, ImageUrl):
    if len(ImageUrl) <= 4:
      print("INFO: 传输的声音路径有误")
      return
    self.payLoad["ToUserName"] = ToUserName
    self.payLoad["VoiceUrl" if "http" == ImageUrl[0:5] else "VoicePath"]=ImageUrl
    #后端生成声音的时候记住不能以http开头
    self.sendPayload("SendVoice")
  
  def sendEmoji(self, ToUserName, EmojiMd5, EmojiLen):
    self.payLoad["ToUserName"] = ToUserName
    self.payLoad["EmojiMd5"] = EmojiMd5
    self.payLoad["EmojiLen"] = EmojiLen
    self.sendPayload("SendEmoji")

  def sendCdnImage(self, ToUserName, XmlStr):
    self.payLoad["ToUserName"] = ToUserName
    self.payLoad["XmlStr"] = XmlStr
    self.sendPayload("SendCdnImage")

  def sendVideo(self, ToUserName, VideoXml):
    self.payLoad["ToUserName"] = ToUserName
    self.payLoad["VideoXml"] = VideoXml
    self.sendPayload("SendVideo")
