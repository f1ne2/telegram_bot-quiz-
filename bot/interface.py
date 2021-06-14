from abc import ABCMeta, abstractmethod


class FormalInterface(metaclass=ABCMeta):
    @abstractmethod
    def push(self, chai_id: str, value: str):
        pass

    @abstractmethod
    def delete(self, chat_id: str):
        pass

    @abstractmethod
    def exist(self, chat_id: str):
        pass

    @abstractmethod
    def len(self, chat_id: str):
        pass

    @abstractmethod
    def range(self, chat_id: str):
        pass
