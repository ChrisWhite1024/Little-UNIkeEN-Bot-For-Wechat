import importlib
import os
import logging
from utils.standardPlugin import *

class PluginManager:

    def __init__(self, pluginsPath: str = "plugins"):
        """
        初始化插件管理器

        Args:
            pluginsPath (str): 存放插件的相对路径
        """
        self.__pluginsPath = pluginsPath
        self.__plugins = {}

        self.__loadedPluginNumber = 0

    def loadAllPlugins(self):
        """
        加载插件文件夹下的所有插件
        """
        pluginList = os.listdir(self.__pluginsPath)
        for plugin in pluginList:
            pluginPath = os.path.join(self.__pluginsPath, plugin)
            if os.path.isdir(pluginPath) and "__init__.py" in os.listdir(pluginPath):
                self.loadPlugin(plugin)
    

    def loadPlugin(self, pluginName: str):
        """
        加载特定插件

        Args:
            pluginName (str): 插件名
        """
        spec = importlib.util.spec_from_file_location(pluginName, os.path.join(self.__pluginsPath, f"{pluginName}", "__init__.py"))
        pluginModule = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(pluginModule)

        if not self.isLegalPlugin(pluginModule):
            logging.warning(f"未成功加载插件{pluginModule.__name__}") 
            return False
        
        self.__plugins[pluginName] = pluginModule
        self.__loadedPluginNumber += 1
        

    def unloadPlugin(self, pluginName: str):
        if pluginName in self.__plugins:
            del self.__plugins[pluginName]
        else:
            logging.error(f"未找到插件: {pluginName}")
        
    def reloadPlugin(self, pluginName: str):
        self.unloadPlugin(pluginName)
        self.loadPlugin(pluginName)

    def isLegalPlugin(self, pluginModule: Any):
        """
        判断 importlib 导入的插件是否合法

        Args:
            pluginModule (Any): importlib.util.module_from_spec 导入的插件模块
        """
        # 判断插件是否包含特定对象
        objects = ['Plugin', 'PLUGIN_INFO']
        for object in objects:
            if not hasattr(pluginModule, object):
                logging.warning(f"插件 {pluginModule.__name__} 未包含 {object} 对象")
                return False

        # 判断插件是否继承抽象基类
        if not issubclass(pluginModule.Plugin, StandardPlugin):
            logging.warning(f"{pluginModule.__name__} 中的 Plugin 类不是 StandardPlugin 的子类")
            return False

        # 检查插件类型是否正确
        pluginType = pluginModule.PLUGIN_INFO['type']
        if not isinstance(pluginType, PluginType):
            logging.warning(f"插件 {pluginModule.__name__} 的 PLUGIN_INFO 对象存在不合法的 'type' 值: {pluginType}")
            return False
        
        return True