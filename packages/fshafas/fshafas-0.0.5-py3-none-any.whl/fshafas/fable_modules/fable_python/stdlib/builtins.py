from abc import abstractmethod
import builtins
from typing import (Protocol, Any, TypeVar, Optional)

_A_ = TypeVar("_A_")

class TextIOBase(Protocol):
    pass

class TextIOWrapper(TextIOBase):
    pass

class IExports(Protocol):
    @abstractmethod
    def chr(self, __arg0: int) -> str:
        ...
    
    @abstractmethod
    def float(self, __arg0: Any) -> float:
        ...
    
    @abstractmethod
    def id(self, __arg0: Any) -> int:
        ...
    
    @abstractmethod
    def int(self, __arg0: Any) -> int:
        ...
    
    @abstractmethod
    def len(self, __arg0: Any) -> int:
        ...
    
    @abstractmethod
    def ord(self, __arg0: str) -> int:
        ...
    
    @abstractmethod
    def print(self, obj: Any) -> None:
        ...
    
    @abstractmethod
    def str(self, __arg0: Any) -> str:
        ...
    

def print(obj: Optional[_A_]=None) -> None:
    builtins.print(obj)


