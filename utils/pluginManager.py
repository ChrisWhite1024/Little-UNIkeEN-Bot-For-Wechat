import importlib
import os
import logging
from utils.standardPlugin import *

class PluginManager:

    def __init__(self, pluginsPath = "plugins"):
        self.__pluginsPath = pluginsPath
        self.__plugins = {}

        self.__loadedPluginNumber = 0

    def loadAllPlugins(self):

        pluginList = os.listdir(self.__pluginsPath)
        for plugin in pluginList:
            # 兼容单文件插件
            pluginPath = os.path.join(self.__pluginsPath, plugin)
            if os.path.isfile(pluginPath) and plugin[-3:] == '.py':
                # 如果存在同名的文件夹插件，那么跳过这个单文件插件加载文件夹插件
                if os.path.isdir(pluginPath.rsplit('.', 1)[0]):
                    continue
                self.__loadedPluginNumber += 1

            if os.path.isdir(pluginPath) and "__init__.py" in os.listdir(pluginPath):
                None
        None
    

    def loadPlugin(self, pluginName):
        spec = importlib.util.spec_from_file_location(pluginName, f"{self.__pluginsPath}/{pluginName}.py")
        pluginModule = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(pluginModule)
        self.__plugins[pluginName] = pluginModule

    def unloadPlugin(self, pluginName):
        if pluginName in self.__plugins:
            del self.__plugins[pluginName]

    def reloadPlugin(self, pluginName):
        self.unloadPlugin(pluginName)
        self.loadPlugin(pluginName)

    def getPlugin(self, pluginName):
        return self.__plugins.get(pluginName)

    def isLegalPlugin(self, pluginModule):
        # 判断插件是否包含特定对象
        objects = ['Plugin', 'PLUGIN_INFO']
        for object in objects:
            if not hasattr(pluginModule, object):
                logging.warning(f"Plugin {pluginModule.__name__} does not have a {object} object")
                return False

        # 判断插件是否继承抽象基类
        if not issubclass(pluginModule.Plugin, StandardPlugin):
            logging.warning(f"Plugin class in {pluginModule.__name__} is not a subclass of StandardPlugin")
            return False
        
        # 判断 PLUGIN_INFO 是否为字典同时是否包含特定键
        if not isinstance(pluginModule.PLUGIN_INFO, dict):
            logging.warning(f"Plugin {pluginModule.__name__}'s PLUGIN_INFO attribute is not a dictionary")

        requiredKeys = ['name', 'version', 'description', 'author', 'type']
        for key in requiredKeys:
            if key not in pluginModule.PLUGIN_INFO:
                logging.warning(f"Plugin {pluginModule.__name__}'s PLUGIN_INFO does not have a '{key}' key")
                return False

        # 检查插件类型是否正确
        pluginType = pluginModule.PLUGIN_INFO['type']
        if not isinstance(pluginType, PluginType):
            logging.warning(f"Plugin {pluginModule.__name__}'s PLUGIN_INFO has an invalid 'type' value: {pluginType}")
            return False
        
        return True