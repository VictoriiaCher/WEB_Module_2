from abc import ABC, abstractmethod


class BookInterface(ABC):
    @abstractmethod
    def show_all(self):
        raise NotImplementedError

    @abstractmethod
    def show_one(self):
        raise NotImplementedError

    @abstractmethod
    def show_page(self):
        raise NotImplementedError
