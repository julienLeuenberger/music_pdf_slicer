from __future__ import annotations # to avoid problem with forward reference between Observer and Subject
from abc import ABC, abstractmethod

class Observer(ABC):
    @abstractmethod
    def update(self, subject:Subject) -> None:
        pass 

class Subject(ABC):
    @abstractmethod
    def attach(self, observer: Observer)->None:
        pass
    @abstractmethod
    def detach(self, observer: Observer)->None:
        pass
    @abstractmethod
    def notify(self)->None:
        pass

