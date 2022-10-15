import os
import time
import av
import pilk
import requests
import random
import librosa
import soundfile as sf
from typing import Union, Any
from utils.runtime import Runtime
from utils.standardPlugin import StandardPlugin

PLUGIN_INFO = {
    'name' : '早安&晚安',
    'version' : '0.4.0',
    'description' : '想要听胡桃说早安/晚安吗\n发送 [早安] [晚安] 试试吧\nPS:因API问题语音功能暂时下线',
    'author' : 'UNIkeEN',
    'type' : 3,
}

GOODMORNING_LIST = [
    "时间最会骗人，但也能让你明白，这个世界没有什么不能失去的，离去的都是风景，留下的才是人生，走到最后的，就是对的人。早安！",
    "善良和爱都是免费的，但不是廉价的，你的善良，需要带点锋芒，你的爱，需要带些理智，带眼识人，毕竟不是所有人都配拥有它们。早安！",
    "人生最好的状态，是每天醒来，面朝阳光，嘴角上扬。不羡慕谁，不讨好谁，默默努力，活成自己想要的模样。早安！",
    "千万不要对任何事感到后悔，因为它曾经一度就是你想要的。后悔没用，要么忘记，要么努力。早安！",
    "有时候，努力一点，是为让自己有资格，不去做不喜欢的事；是为了能让自己，遇见一个喜欢的人时，不会因为自己不够好而没能留住对方。早安！",
    "该来的都会来，该走的全会走，别抗拒，别挽留，别贪恋。学着看淡一些事情。亲爱的，愿你像向日葵一样，每天都充满正能量，开始元气满满的一天。",
    "世界上根本就不存在完美的事物，我们没必要浪费大量的精力去寻找不存在的东西。与其用一生的时间去执着地追求虚无缥缈的东西，不如珍惜和把握现在美好的生活。",
    "每个人的人生里都会遇到一场措手不及的大雨，若你身陷雨中，愿有人为你撑伞；如果没有，也愿你有听雨的心情。早安！",
    "美好的事情总会到来，你要简单干净聪明单纯，就会发现奇迹不是降临，它是因你而来。",
    "人这辈子，有人羡慕你，有人讨厌你，有人嫉妒你，有人看不起你，没关系，他们都是外人；生活就是这样，你所做的一切不能让每个人都满意。不要为了讨好别人，而丟失自己的本性。早安！",
    "一个人至少应该拥有一个梦想，有一个理由去坚强，心若没有栖息的地方，在哪里都是流浪。早安！",
    "一万个美丽的未来，抵不上一个温暖的现在。早安！",
    "愿你成为自己喜欢的样子，不抱怨，不将就，有野心，有光芒！早安！",
    "无论生活怎样，都不要忘记微笑，愿你成为自己的太阳，无需凭借谁的光。",
    "不管昨天有多糟糕，不要让它影响你的现在和未来，活得像向日葵一样灿烂。早上好！",
    "天是冷的，心是暖的，对你的祝福是永远的！人是远的，心是近的，对你的思念是不变的！愿你每一天都阳光灿烂、笑口常开，早安！",
    "抱最大希望，尽最大努力，做最坏打算，持最好心态。记住该记住的，忘记该忘记的，改变能改变的，接受成事实的。太阳总是新的，每天都是美好的日子。早安！",
    "每天清晨的第一道曙光，可以神奇地治愈昨日的伤痛。",
    "带着阳光出发，去遇见温暖；带着微笑前行，去遇见幸福，所有美好的不期而遇，都在路上。新的一天，早安！",
]

GOODNIGHT_LIST = [
    "今夜我要去征拯救地球，有事请留言。晚安！",
    "黑夜不会亏待晚睡的人，它会让你脱发。晚安！",
    "我的小脑袋已经忙了一天了，好累啊，也该休息了。晚安！",
    "把所有的烦恼都抛掉，拉上窗帘，挂上月亮，好好睡一觉。晚安！",
    "你想一夜暴富吗？那就跟我一起关灯睡觉吧。晚安！你想一夜暴富吗？那就跟我一起关灯睡觉吧。晚安！",
    "我已经盖好了被子，闭好一只眼，就等你说晚安了，说完我就闭另一只了。",
    "要开心，要努力，要像星星一样发光发亮。晚安！",
    "把星星熬成糖浆，蘸一蘸你说过的晚安，然后大口大口的吃掉。晚安！",
    "我要乔装成一颗小奶糖，夜深了提着星星灯快快溜到你的梦里，嘻嘻，晚安！",
    "你知道为什么我在夜里总是不睡觉吗？因为黑夜需要我这颗闪亮的星。晚安！",
    "早点睡吧，今晚我会跑到你的梦里手舞足蹈。晚安！",
    "要不要一起去梦中看月亮，一定超级大，超级美。晚安！",
    "月亮不睡觉，我也不睡觉，我是这个世界上的一个小美味。",
    "疲惫的生活需要一个温柔的梦和一个很爱的人。晚安！",
    "这个世界太危险，时间就该浪费在美好的事物上。晚安！",
    "世事千帆过，前方终会是温柔和月光。晚安！",
    "当你在夜晚孤军奋战时，漫天星光因为你而闪烁。晚安！",
    "你就是天赐的礼物，我迟来的救赎；你是不灭的星光，日复一日的美梦。晚安！",
    ".我在人间贩卖黄昏，只为收集世间温柔去见你，晚安！",
    "今天的世界已经打烊了，已经不对外营业了，晚安！",
    "愿你从此不对新事畏惧，不会重蹈覆辙，再也不为感情沉沦，不为熬夜后悔，相信有人会陪你颠沛流离，如果没有，愿你成为自己的太阳。晚安，好梦！",
    "错过落日余晖，还会有满天星辰，只要不放弃，最差就是大器晚成。愿你全力以赴，且满载而归！晚安！",
    "最好的年龄是，那一天，你终于知道并且坚信自己有多好，不是虚张，不是夸浮，不是众人捧，是内心明明澈澈知道：是的，我就是这么好。晚安！",
    "夜深人静了就把心掏出来自己缝缝补补，完事了再塞回去，睡一觉醒来又是信心百倍。晚安！",
    "所有的故事，都有一个结局。但幸运的是，在生活中，每个结局都会变成一个新的开始。晚安!",
    "难过的时候，就把自己当成另一个人，当初怎么安慰别人，现在就怎么安慰自己。晚安！",
    "晚是世界的晚，安是有你的安。晚安！",
    "希望生活有惊喜，希望喜欢被回应，愿你好梦，晚安！",
    "原来以为，拥有的东西越多，才会越幸福，后来才发现，生活越简单，才会更轻松。晚安好梦。",
    "星星会不会趁着人间的烟火坠落时，偷偷溜下来见想见的人。晚安！",
    "今夜太晚了，明天继续想你，等星星都睡着了，再说想你。",
    """我对世界说晚安，唯独对你说喜欢！爱你！""",
    "好想抱抱你呀~只是因为心疼你，觉得你该休息了，然后在你措不及防的时候拥你入怀，揉揉你的头发告诉你：已经够了，你很努力了可以好好休息了",
    "晚安，换个世界想你，一会儿见。",
    "今天月亮不营业，所以由我来说晚安。",
    "趁着星星和月亮都在，悄悄说声，你真可爱，晚安。",
    "想对全世界说晚安，恰好你就是全世界。",
    "想要劫持一颗星星，在月色朦胧的夜晚降落到你的梦里",
    "晚安唔西迪西，晚安玛卡巴卡，晚安依古比古，晚安汤姆布利波，晚安小点点，晚安叮叮车，晚安哈呼呼晚安飞飞鱼，晚安我的朋友们。",
    "睡觉吧，你的头发不允许你瞎想w",
    "今晚来我的梦里吗？谈恋爱的那种。",
    "你知道吗？我有一个心愿，那就是以后能够从你的房间跟你一起看星星。",
    "想做你床边的小熊，为你打败梦里的恶龙。",
    "今天这皎洁的月光和满天的星辰都归你，而我也归你。",
    "晚安，我带着我的可爱一起打烊了，帮我关一下月亮",
]

class Plugin(StandardPlugin):
    def judgeTrigger(msg:str, data:Any) -> bool:
        return msg == "早安" or msg == "晚安" 
    def executeEvent(msg:str, data:Any, runtime:Runtime) -> Union[None, str]:
        # 删除过多的音频文件
        fileList = os.listdir('data/pluginData/greetings')
        if len(fileList) > 15:
            for file in fileList:
                os.remove(os.path.join('data/pluginData/greetings', file))
                
        ran = random.randint(1, 10)
        if msg == "早安":
            sentence = random.choice(GOODMORNING_LIST)
            runtime.msgQueue.sendMsg(f"{data['FromUserName']}", sentence)
            """
            if ran > 4:
                runtime.msgQueue.sendMsg(f"{data['FromUserName']}", sentence)
            else:
                silk_path = send_genshin_voice(sentence)
                runtime.msgQueue.sendVoice(f"{data['FromUserName']}", silk_path)
            """
        if msg == "晚安":
            sentence = random.choice(GOODNIGHT_LIST)
            runtime.msgQueue.sendMsg(f"{data['FromUserName']}", sentence)
            """
            if ran > 4:
                runtime.msgQueue.sendMsg(f"{data['FromUserName']}", sentence)
            else:
                silk_path = send_genshin_voice(sentence)
                runtime.msgQueue.sendVoice(f"{data['FromUserName']}", silk_path)
            """
        return "OK"


def send_genshin_voice(sentence):
    timeNow = time.time()
    speaker = '胡桃'
    response = requests.get(f"http://233366.proxy.nscc-gz.cn:8888/?text={sentence}&speaker={speaker}&length_factor=0.5&noise=0.4&format=wav")
    file_path = "data/pluginData/greetings/{}.wav".format(timeNow)
    silk_path = "data/pluginData/greetings/c{}.silk".format(timeNow)
    convert_path = "data/pluginData/greetings/c{}.wav".format(timeNow) # 重采样文件地址
    with open(file_path, "wb") as code:
        code.write(response.content)
    audio, sr = librosa.load(file_path, sr=None)
    audio_24k = librosa.resample(audio, orig_sr=22050, target_sr=24000)
    sf.write(convert_path, audio_24k, 24000)
    convert_to_silk(convert_path)
    return silk_path


def to_pcm(in_path: str) -> tuple[str, int]:
    """任意媒体文件转 pcm"""
    out_path = os.path.splitext(in_path)[0] + '.pcm'
    with av.open(in_path) as in_container:
        in_stream = in_container.streams.audio[0]
        sample_rate = in_stream.codec_context.sample_rate
        with av.open(out_path, 'w', 's16le') as out_container:
            out_stream = out_container.add_stream(
                'pcm_s16le',
                rate=sample_rate,
                layout='mono'
            )
            try:
               for frame in in_container.decode(in_stream):
                  frame.pts = None
                  for packet in out_stream.encode(frame):
                     out_container.mux(packet)
            except:
               pass
    return out_path, sample_rate


def convert_to_silk(media_path: str) -> str:
    """任意媒体文件转 silk, 返回silk路径"""
    pcm_path, sample_rate = to_pcm(media_path)
    silk_path = os.path.splitext(pcm_path)[0] + '.silk'
    pilk.encode(pcm_path, silk_path, pcm_rate=sample_rate, tencent=True)
    os.remove(pcm_path)
    return silk_path