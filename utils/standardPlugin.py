from abc import ABC, abstractmethod
from typing import Union, Tuple, Any
from utils.runtime import Runtime

class StandardPlugin(ABC):
    @staticmethod
    @abstractmethod
    def judgeTrigger(msg: str, data: Any) -> bool:
        """
        @msg: message input
        @return: whether trigger this class
        """
    @staticmethod
    @abstractmethod
    def executeEvent(msg: str, data: Any, runtime: Runtime) -> Union[None, str]:
        """
        """