from utils.preLoader import PreLoader
from utils.msgQueue import MsgQueue
from singleton_decorator import singleton

@singleton
class Runtime():
    def __init__(self) -> None:
        self.preLoader = PreLoader()
        self.msgQueue = MsgQueue()
