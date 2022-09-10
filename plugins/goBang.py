from typing import Union, Any
import requests
import json
from utils.basicEvent import *
from utils.basicConfigs import *
from utils.functionConfigs import *
from utils.standardPlugin import StandardPlugin
import urllib.parse

class GoBangGame():
    def __init__(self, id):
        self.ROWS = 17
        self.COLS = 17
        self.id = id # 群聊/私聊 id
        self.checkerboard = [[0]*self.ROWS]*self.COLS
    def refreshCheckboard(self):
        self.checkerboard = [[0]*self.ROWS]*self.COLS
    