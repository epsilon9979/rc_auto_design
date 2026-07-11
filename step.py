from abc import ABC
from abc import abstractmethod

class STEPS(ABC):
    def __init__(self):
        pass
    
    @abstractmethod
    def process(self, data, database):
        pass
 
class STEPexception(Exception):
    pass