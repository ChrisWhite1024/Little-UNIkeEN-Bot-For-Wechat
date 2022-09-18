from utils.preLoader import PreLoader
from utils.msgQueue import MsgQueue

class Runtime():
    def __init__(self) -> None:
        self.preLoader = PreLoader()
        self.msgQueue = MsgQueue()
