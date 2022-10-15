import requests
import os
import json
import importlib

class PreLoader():

    __PLUGINS_PATH = 'plugins'
    __CONFIGS_PATH = 'configs'
    __CHATROOM_CONF_PATH = 'configs/ChatRoomConf'  
    __USER_CONF_PATH = 'configs/UserConf'
    __GLOBAL_CONF_PATH = 'config.json'
    __GLOBAL_CONF_DEFAULT = {
        'Version' : '0.3.9',
        'UpdateLog' : 'WhiteBot最初版本，感谢大家的支持',
        'SERVER_IP' : '',
        'SERVER_PORT' : '',
        'WXID' : ''
    }
    # 存储默认配置文件
    __USER_CONF_DEFAULT = {}
    __CHATROOM_CONF_DEFAULT = {}
    # 存储运行时配置信息
    __USER_CONF_RUNTIME = {}
    __CHATROOM_CONF_RUNTIME = {}
    __GLOBAL_CONF_RUNTIME = {}
    # 存储插件对象
    CHATROOM_MODULE_LIST = {}
    USER_MODULE_LIST = {}

    def __init__(self) -> None:
        # 加载插件
        if not os.path.exists('configs'):
            os.mkdir('configs') 
        if not os.path.exists(self.__PLUGINS_PATH):
            os.mkdir(self.__PLUGINS_PATH)
        if not os.path.exists(self.__CHATROOM_CONF_PATH):
            os.mkdir(self.__CHATROOM_CONF_PATH)
        if not os.path.exists(self.__USER_CONF_PATH):
            os.mkdir(self.__USER_CONF_PATH)
        if not os.path.exists(self.__CONFIGS_PATH):
            os.mkdir(self.__CONFIGS_PATH)
            
        pluginList = os.listdir(self.__PLUGINS_PATH)
        totalPluginNumber = 0
        loadedPluginNumber = 0
        closedPluginNumber = 0
        for file in pluginList:
            if file[-3:] == '.py':
                totalPluginNumber += 1

                module_spec = importlib.util.spec_from_file_location(f'{file[:-3]}', os.path.join(self.__PLUGINS_PATH, file))
                module = importlib.util.module_from_spec(module_spec)
                module_spec.loader.exec_module(module)

                # 插件合法性判断
                isLegal = True
                if dir(module).count('Plugin') == 0:
                    isLegal = False
                    print(f'[W] (preLoader.py)PreLoader：{file}插件未加载，缺少Plugin类')
                if dir(module).count('PLUGIN_INFO') == 0:
                    isLegal = False
                    print(f'[W] (preLoader.py)PreLoader：{file}插件未加载，缺少PLUGIN_INFO对象')

                if isLegal:
                    if module.Plugin.__base__.__name__ != 'StandardPlugin':
                        isLegal = False
                        print(f'[W] (preLoader.py)PreLoader：{file}插件未加载，找不到StandardPlugin父类') 
                    try:
                        module.PLUGIN_INFO['name']
                        module.PLUGIN_INFO['version']
                        module.PLUGIN_INFO['description']
                        module.PLUGIN_INFO['author']
                        module.PLUGIN_INFO['type']
                    except:
                        print(f'[W] (preLoader.py)PreLoader：{file}插件未加载，PLUGIN_INFO键错误')
                        isLegal = False
                    try:
                        if type(module.PLUGIN_INFO['name']) != str or type(module.PLUGIN_INFO['description']) != str or type(module.PLUGIN_INFO['version']) != str or type(module.PLUGIN_INFO['author']) != str:
                           isLegal = False 
                           print(f'[W] (preLoader.py)PreLoader：{file}插件加载失败，PLUGIN_INFO值类型错误')
                        if type(module.PLUGIN_INFO['type']) != int or module.PLUGIN_INFO['name'] > 4 or module.PLUGIN_INFO['name'] < 1:
                           isLegal = False 
                           print(f'[W] (preLoader.py)PreLoader：{file}插件加载失败，PLUGIN_INFO值越界')
                    except:
                        pass
                    
                # 初始化插件对象
                if isLegal:
                    if module.PLUGIN_INFO['type'] == 4:   
                        print(f'[L] (preLoader.py)PreLoader：{file}插件已关闭')
                        closedPluginNumber += 1
                    if module.PLUGIN_INFO['type'] == 1:    
                        self.CHATROOM_MODULE_LIST.setdefault(file, module)
                        print(f'[L] (preLoader.py)PreLoader：{file}插件加载成功')
                        loadedPluginNumber += 1
                    if module.PLUGIN_INFO['type'] == 2:
                        self.USER_MODULE_LIST.setdefault(file, module)
                        print(f'[L] (preLoader.py)PreLoader：{file}插件加载成功')
                        loadedPluginNumber += 1
                    if module.PLUGIN_INFO['type'] == 3:
                        self.CHATROOM_MODULE_LIST.setdefault(file, module)
                        self.USER_MODULE_LIST.setdefault(file, module)
                        print(f'[L] (preLoader.py)PreLoader：{file}插件加载成功')
                        loadedPluginNumber += 1
        print(f'[L] (preLoader.py)PreLoader：插件加载完成，共加载[{loadedPluginNumber}/{totalPluginNumber}]个插件，{totalPluginNumber - loadedPluginNumber - closedPluginNumber}个插件加载失败, {closedPluginNumber}个插件已关闭\n')

        # -------------------------------------------------------------------------------------------------------------------------
        # 初始化全局配置文件
        globalConfig = {}
        if os.path.isfile(self.__GLOBAL_CONF_PATH): # 检验配置文件是否存在
            try:
                # 检查JSON合法性
                with open(self.__GLOBAL_CONF_PATH, 'r') as f1:
                    globalConfig = json.load(f1)
                if len(globalConfig) != len(self.__GLOBAL_CONF_DEFAULT):
                    raise IOError
                for object in globalConfig.items():
                    if type(globalConfig[object[0]]) != type(self.__GLOBAL_CONF_DEFAULT[object[0]]):
                        raise IOError
                self.__GLOBAL_CONF_RUNTIME = globalConfig


                # 检验服务可用性 可移植性差
                try:
                    testUrl = "http://{}:{}/v1/LuaApiCaller?funcname=InitWxids&timeout=10&wxid={}".format(self.__GLOBAL_CONF_RUNTIME['SERVER_IP'], self.__GLOBAL_CONF_RUNTIME['SERVER_PORT'], self.__GLOBAL_CONF_RUNTIME['WXID'])
                    payload = json.dumps({
                        "CurrentWxcontactSeq": 0,
                        "CurrentChatRoomContactSeq": 0
                    })
                    headers = {
                        'Content-Type': 'application/json'
                    }
                    response = requests.request("POST", testUrl, headers=headers, data=payload, timeout=5)
                    if response.json().get('ErrMsg', False):
                        print(f'[E] (preLoader.py)PreLoader：成功连接框架但WXID未登录，程序已退出')
                        exit()
                    else:
                        print(f'[L] (preLoader.py)PreLoader：全局配置文件读取成功')
                        print(f'[L] (preLoader.py)PreLoader：检查框架连接状态成功')

                except Exception as e:
                    # print(e)
                    print(f'[E] (preLoader.py)PreLoader：连接失败，可能是服务器框架不可用、网络环境差或服务器地址填写错误，程序已退出')
                    exit()


            except Exception as e:
                # print(e)
                with open(self.__GLOBAL_CONF_PATH, 'w') as f1:
                    json.dump(self.__GLOBAL_CONF_DEFAULT, f1, indent = 4)
                    print(f'[E] (preLoader.py)PreLoader：全局配置文件config.json加载失败，已重新生成，填写配置文件并重启程序以继续')
                    exit()
        else: # 生成配置文件
            with open(self.__GLOBAL_CONF_PATH, 'w') as f1:
                json.dump(self.__GLOBAL_CONF_DEFAULT, f1, indent = 4)
                print(f'[E] (preLoader.py)PreLoader：全局配置文件config.json不存在，已重新生成，填写配置文件并重启程序以继续')
                exit()

        # -------------------------------------------------------------------------------------------------------------------------
        # ！仍然需要解决配置文件无法及时更新的问题
        # 初始化用户配置文件
        for object in self.USER_MODULE_LIST.items():
            pluginConfig = {}
            pluginConfig.setdefault('name', object[1].PLUGIN_INFO['name'])
            pluginConfig.setdefault('version', object[1].PLUGIN_INFO['version'])
            pluginConfig.setdefault('author', object[1].PLUGIN_INFO['author'])
            pluginConfig.setdefault('enabled', True)
            self.__USER_CONF_DEFAULT.setdefault(object[0], pluginConfig)
        
        # 更新用户配置文件
        print(f'[L] (preLoader.py)PreLoader：更新用户配置文件')
        userConfigPath = os.path.join(self.__USER_CONF_PATH, 'config.json')
        try:
            if os.path.isfile(userConfigPath):
                with open(userConfigPath, "r") as f1:
                    userConfig = json.load(f1)
                for value in self.__USER_CONF_DEFAULT.items():
                    if userConfig.get(value[0], False):
                        pass
                    # 在原配置文件中找不到键 既写入新插件配置
                    else:
                        while 1:
                            inputJudge = input(f'[A] (preLoader.py)PreLoader：检测到适用于用户的新插件{value[0]}，是否在{userConfigPath}中开启[Y/N]:')
                            
                            if inputJudge == 'Y' or inputJudge == 'y':
                                userConfig.setdefault(value[0], value[1])
                                break
                            if inputJudge == 'N' or inputJudge == 'n':
                                pluginConfig = {}
                                pluginConfig.setdefault('name', value[1]['name'])
                                pluginConfig.setdefault('version', value[1]['version'])
                                pluginConfig.setdefault('enabled', False)
                                userConfig.setdefault(value[0], pluginConfig)
                                break
                        with open(userConfigPath, 'w') as f2:
                            json.dump(userConfig, f2, indent = 4)
                            print(f'[L] (preLoader.py)PreLoader：写入{userConfigPath}文件成功')
                # 删除不存在的插件配置
                deleteKey = []
                for value in userConfig.items():
                    if self.__USER_CONF_DEFAULT.get(value[0], False):
                        for attribute in self.__USER_CONF_DEFAULT[value[0]]:
                            if attribute == 'enabled':
                                pass
                            else:
                                if userConfig[value[0]][attribute] != self.__USER_CONF_DEFAULT[value[0]][attribute]:
                                    userConfig[value[0]][attribute] = self.__USER_CONF_DEFAULT[value[0]][attribute]
                                    with open(userConfigPath, 'w') as f2:
                                        json.dump(userConfig, f2, indent = 4)            
                    else:
                        deleteKey.append(value[0]) 
                for key in deleteKey:
                    userConfig.pop(key)
                    with open(userConfigPath, 'w') as f2:
                        json.dump(userConfig, f2, indent = 4)
                    print(f'[L] (preLoader.py)PreLoader：适用于用户的插件{key}未加载，已从{userConfigPath}中移除')
                self.__USER_CONF_RUNTIME = userConfig
            # 路径下找不到文件时执行
            else:
                with open(userConfigPath, 'w') as f3:
                    json.dump(self.__USER_CONF_DEFAULT, f3, indent = 4)
                    print(f'[L] (preLoader.py)PreLoader：成功建立{userConfigPath}文件')
                self.__USER_CONF_RUNTIME = self.__USER_CONF_DEFAULT
        # 无法读取JSON时执行
        except Exception as e:
            # print(e)
            with open(userConfigPath, 'w') as f4:
                json.dump(self.__USER_CONF_DEFAULT, f4, indent = 4)
            print(f'[E] (preLoader.py)PreLoader：{userConfigPath}读取失败，JSON文件已重置')
            self.__USER_CONF_RUNTIME = self.__USER_CONF_DEFAULT

        
        print(f'[L] (preLoader.py)PreLoader：用户配置文件更新成功\n')

        # -------------------------------------------------------------------------------------------------------------------------
        # 初始化群聊配置文件
        for object in self.CHATROOM_MODULE_LIST.items():
            pluginConfig = {}
            pluginConfig.setdefault('name', object[1].PLUGIN_INFO['name'])
            pluginConfig.setdefault('version', object[1].PLUGIN_INFO['version'])
            pluginConfig.setdefault('author', object[1].PLUGIN_INFO['author'])
            pluginConfig.setdefault('enabled', False)
            self.__CHATROOM_CONF_DEFAULT.setdefault(object[0], pluginConfig)

        
        print(f'[L] (preLoader.py)PreLoader：更新群聊配置文件')
        for chatroomDir in os.listdir(self.__CHATROOM_CONF_PATH):
            if (os.path.isdir(os.path.join(self.__CHATROOM_CONF_PATH, chatroomDir))):
                chatroomConfigPath = os.path.join(self.__CHATROOM_CONF_PATH, chatroomDir, 'config.json')
                if os.path.isfile(chatroomConfigPath):
                    try:
                        with open(chatroomConfigPath, 'r') as f:
                            chatroomConfig = json.load(f) 
                        for value in self.__CHATROOM_CONF_DEFAULT:
                            if chatroomConfig.get(value, False):
                                pass
                            else:
                                chatroomConfig.setdefault(value, self.__CHATROOM_CONF_DEFAULT[value])
                                with open(chatroomConfigPath, 'w') as f2:
                                    json.dump(chatroomConfig, f2, indent = 4)
                                print(f'[L] (preLoader.py)PreLoader：检测到适用于群聊的新插件，写入{chatroomConfigPath}文件成功，插件已默认关闭')
                        # 删除不存在的插件配置
                        deleteKey = []
                        for value in chatroomConfig:
                            #更新插件变更
                            if self.__CHATROOM_CONF_DEFAULT.get(value, False):
                                for attribute in self.__CHATROOM_CONF_DEFAULT[value]:
                                    if attribute == 'enabled':
                                        pass
                                    else:
                                        if chatroomConfig[value][attribute] != self.__CHATROOM_CONF_DEFAULT[value][attribute]:
                                            chatroomConfig[value][attribute] = self.__CHATROOM_CONF_DEFAULT[value][attribute]
                                            with open(chatroomConfigPath, 'w') as f2:
                                                    json.dump(chatroomConfig, f2, indent = 4) 
                            else:
                                deleteKey.append(value) 
                        for key in deleteKey:
                            chatroomConfig.pop(key)
                            with open(chatroomConfigPath, 'w') as f2:
                                json.dump(chatroomConfig, f2, indent = 4)
                            print(f'[L] (preLoader.py)PreLoader：适用于群聊的插件{key}未加载，已从{chatroomConfigPath}中移除')
                        
                        self.__CHATROOM_CONF_RUNTIME[chatroomDir] = chatroomConfig
                        
                    except:
                        with open(chatroomConfigPath, 'w') as f4:
                            json.dump(self.__CHATROOM_CONF_DEFAULT, f4, indent = 4)
                        self.__CHATROOM_CONF_RUNTIME.setdefault(chatroomDir, self.__CHATROOM_CONF_DEFAULT)
                        print(f'[E] (preLoader.py)PreLoader：{chatroomConfigPath}读取失败，JSON文件已重置')
        print(f'[L] (preLoader.py)PreLoader：更新群聊配置文件成功')        
        # -------------------------------------------------------------------------------------------------------------------------

    def getGlobalConfig(self, key: str):
        return self.__GLOBAL_CONF_RUNTIME[key]

    def isUserPluginEnabled(self, plugin: str):
        if self.__USER_CONF_RUNTIME.get(plugin, False):
            return self.__USER_CONF_RUNTIME[plugin]['enabled']
        else:
            print(f'[E] (preLoader.py)PreLoader：内部错误，不存在的用户插件，程序已退出') 
            exit()
    # 检验群聊插件是否开启，若为新群聊则更新RUNTIME与配置文件
    def isChatRoomPluginEnabled(self, plugin: str, chatroom: str):
        if self.__CHATROOM_CONF_RUNTIME.get(chatroom, False):
            if self.__CHATROOM_CONF_RUNTIME[chatroom].get(plugin, False):
                return self.__CHATROOM_CONF_RUNTIME[chatroom][plugin]['enabled']
            else:
                print(f'[E] (preLoader.py)PreLoader：内部错误，不存在的用户插件，程序已退出') 
                exit()
        else:
            print(f'[L] (preLoader.py)PreLoader：检测到新群聊消息，已生成群聊配置文件，插键已默认关闭，若想开启请修改配置文件并重启WhiteBot')
            os.mkdir(os.path.join(self.__CHATROOM_CONF_PATH, chatroom))
            with open(os.path.join(self.__CHATROOM_CONF_PATH, chatroom, 'config.json'), 'w') as f4:
                json.dump(self.__CHATROOM_CONF_DEFAULT, f4, indent = 4)
            self.__CHATROOM_CONF_RUNTIME[chatroom] = self.__CHATROOM_CONF_DEFAULT
            return False