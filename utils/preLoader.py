import os
import json
import importlib
from sys import flags

class PreLoader():
    PluginList = []
    CONF_DEFAULT = {}
    PLUGINS_PATH = 'plugins'
    CHATROOM_CONF_PATH = 'data/chatroomConf'

    def __init__(self) -> None:
        # 获取插件Py文件列表
        List = os.listdir(self.PLUGINS_PATH)
        for file in List:
            if file[-3:] == '.py':
                module_spec = importlib.util.spec_from_file_location(f'{file[:-3]}', os.path.join(self.PLUGINS_PATH, file))
                module = importlib.util.module_from_spec(module_spec)
                module_spec.loader.exec_module(module)
                # 获取文件中的对象列表
                flag = 0
                for object in dir(module):
                    # print(object[0:8])  
                    if object[0:7] == 'plugin_':
                        # 保证一个Py文件中只有一个plugin_类
                        if flag == 1:
                            self.PluginList.pop()
                            print(f'[E] (preLoader.py)PreLoader：{file}存在两个plugin_类')
                            break
                        # 防止不同文件中类冲突 
                        if self.PluginList.count(object[0:7]) >= 1:
                            print(f'[E] (preLoader.py)PreLoader：{file}中类名与已加载插件冲突，建议修改类名')
                            break
                        else:
                            self.PluginList.append(object[7:])
                            print(f'[L] (preLoader.py)PreLoader：{file}已加载')
                            flag = 1
                if flag == 0:
                    print(f'[E] (preLoader.py)PreLoader：{file}中不存在plugin_类')            
        # 构造默认群配置文件并更新现有配置文件
        List = os.listdir(self.CHATROOM_CONF_PATH)
        for plugin in self.PluginList:
            self.CONF_DEFAULT.setdefault(f'{plugin}', {"enable": True})

        '''
        for d in List:
            if d[-9:] == '@chatroom':
                config_path = os.path.join(self.CHATROOM_CONF_PATH, d, 'config.json')
                # 判断是否有config文件
                if os.path.isfile(config_path):
                    # 添加新插件键值 可优化
                    for plugin in self.PluginList:
                        with open(config_path, 'w+') as f:
                            tmp = json.loads(f)
                            if not tmp.has_key(plugin):
                                tmp.setdefault(plugin, default = {"enable": True})
                                print(f'[L] (preLoader.py)PreLoader：在{config_path}中添加新键{plugin}')
                            f = json.dumps(tmp)
                else:
                    with open(config_path, 'w+') as f:
                        f = json.dumps(self.CONF_DEFAULT)
                        print(f'[L] (preLoader.py)PreLoader：成功创建{config_path}')
        '''

        
            
                        

                
                


                        



