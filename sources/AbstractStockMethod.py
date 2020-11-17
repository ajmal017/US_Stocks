from abc import ABC, abstractmethod

class AbstractStockMethod(ABC):

    @abstractmethod
    def query_by_symbol(self):
        pass

    @abstractmethod
    def get_latest_date(self):
        pass