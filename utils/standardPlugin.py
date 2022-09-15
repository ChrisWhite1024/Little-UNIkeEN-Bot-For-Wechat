from abc import ABC, abstractmethod
from typing import Union, Tuple, Any

class StandardPlugin(ABC):
    @staticmethod
    @abstractmethod
    def judgeTrigger(msg:str, data:Any) -> bool:
        """
        @msg: message input
        @return: whether trigger this class
        """
    @staticmethod
    @abstractmethod
    def executeEvent(msg:str, data:Any) -> Union[None, str]:
        """
        """