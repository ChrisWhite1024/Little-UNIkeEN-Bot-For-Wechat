import queue
import random
import threading
from time import sleep
from utils.basicEvents import Send

class MsgQueue():
    __msgQueue = queue.Queue(maxsize = 0)
    def __init__(self) -> None:
        threading.Thread(target = self.getEvent, daemon = True).start()
    # 发送图片
    def sendImage(self, ToUserName, ImagePath): 
        self.__msgQueue.put((ToUserName, lambda: Send.sendImage(ToUserName, ImagePath)))
    # 发送消息 有待添加@功能
    def sendMsg(self, ToUserName, Content, AtUsers=""): 
        self.__msgQueue.put((ToUserName, lambda: Send.sendMsg(ToUserName,Content)))
    # 发送App消息
    def sendAppMsg(self, ToUserName, Content): 
        self.__msgQueue.put((ToUserName, lambda: Send.sendAppMsg(ToUserName, Content)))
    # 发送语音消息
    def sendVoice(self, ToUserName, VoicePath): 
        self.__msgQueue.put((ToUserName, lambda: Send.sendVoice(ToUserName, VoicePath)))
    # 发送MD5表情
    def sendEmoji(self, ToUserName, EmojiMd5, EmojiLen): 
        self.__msgQueue.put((ToUserName, lambda: Send.sendEmoji(ToUserName, EmojiMd5, EmojiLen)))
    # 发送CDN图片
    def sendCdnImage(self, ToUserName, XmlStr): 
        self.__msgQueue.put((ToUserName, lambda: Send.sendCdnImage(ToUserName, XmlStr)))
    # 发送视频
    def sendVideo(self, ToUserName, VideoXml): 
        self.__msgQueue.put((ToUserName, lambda: Send.sendVideo(ToUserName, VideoXml)))

    def getEvent(self):
        bufferQueue = queue.Queue(maxsize = 2)
        userNameFirst = ''
        userNameSecond = ''
        userNameExecuted = ''
        while True:
            if not bufferQueue.empty(): # 缓冲队列是空的
                if bufferQueue.full(): # 缓冲队列满了
                    func = bufferQueue.get()
                    func()
                    if userNameFirst == userNameSecond:
                        sleep(random.uniform(2, 5))
                    else:
                        sleep(random.uniform(4, 7))
                    userNameExecuted = userNameFirst
                    userNameFirst = userNameSecond
                    userNameSecond = ''
                    if not self.__msgQueue.empty():
                        (userNameSecond, func) = self.__msgQueue.get()
                        bufferQueue.put(func)
                else: # 缓冲队列有一个元素
                    func = bufferQueue.get()
                    func()
                    if userNameExecuted == userNameFirst:
                        sleep(3)
                    else:
                        sleep(5)
                    userNameExecuted = userNameFirst
                    userNameFirst = ''
                    if not self.__msgQueue.empty():
                        (userNameFirst, func) = self.__msgQueue.get()
                        bufferQueue.put(func) 
            else:
                if not self.__msgQueue.empty():
                    (userNameFirst, func) = self.__msgQueue.get()
                    bufferQueue.put(func)




    
