from abc import ABC,abstractmethod

class BaseAlgorithm(ABC):
    @abstractmethod
    def toJson(data):
       pass
    
    @abstractmethod
    def fromJSON():
        pass
