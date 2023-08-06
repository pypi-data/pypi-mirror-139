import abc
from .Sink import Sink

class Command(abc.ABC):

    @abc.abstractmethod
    def do(self, sink: Sink):
        pass