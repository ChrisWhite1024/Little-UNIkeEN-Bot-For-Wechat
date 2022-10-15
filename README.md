# Little-UNIkeEN-Bot-For-Wechat
## 这是什么
Little-UNIkeEN-Bot-For-Wechat是[Little-UNIkeEN-Bot](https://github.com/UNIkeEN/Little-UNIkeEN-Bot)的WeChat分支，是配合 [RSTBot](https://babyqdoc.gitbook.io/wechatdocs/) 使用的WeChat Bot后端，主要作用是与RSTBot接口对接并且响应消息，实现了插件化和对WebAPI请求的封装

## 如何使用
1. 配置好[RSTBot前置框架](https://babyqdoc.gitbook.io/wechatdocs/da-jian-huan-jing-zhi-nan-bi-du)
2. 在根目录config.json中填入RSTBot WebScocket服务端IP和端口以及登录的WXID
3. 根据requirements.txt配置python环境，安装依赖库
4. 在根目录下执行 python main.py

## 配置文件
1. /configs/ChatRoomConf 中存储了单独群聊的配置文件，可以单独控制各群插件的开关，未生成配置文件的群在启动后会进行初始化，插件默认关闭需要手动开启
2. /configs/UserConf 中储存了适用于全局用户的配置文件，若不存在启动时也会初始化

## 编写插件
Little-UNIkeEN-Bot-For-Wechat基于插件来实现全部逻辑，插件的编写规范请参照 /plugins/template.py

## 展望
由于与Little-UNIkeEN-Bot的底层架构不同，只复用了部分组件，当前的插件API与Little-UNIkeEN-Bot有部分区别，下一步会完成插件API统一，更新插件热加载和框架兼容层
