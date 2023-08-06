import abc
from .Command import Command
from .Pipe import Pipe

class PipeBuilder(abc.ABC):
    
    @abc.abstractproperty
    def build(self) -> Pipe:
        pass

    @abc.abstractmethod
    def command(self, command: Command):
        pass