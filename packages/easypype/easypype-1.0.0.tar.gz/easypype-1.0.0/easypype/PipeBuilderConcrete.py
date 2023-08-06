from .Command import Command
from .Pipe import Pipe
from .PipeBuilder import PipeBuilder

class PipeBuilderConcrete(PipeBuilder):

    def __init__(self):
        self.pipe = Pipe()
    
    def build(self) -> Pipe:
        return self.pipe

    def command(self, command: Command):
        self.pipe.commands.append(command)
        return self