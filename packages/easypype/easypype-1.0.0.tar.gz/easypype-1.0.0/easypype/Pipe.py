from .Command import Command
from .Sink import Sink
from multiprocessing.pool import ThreadPool

class Pipe(Command):

    def __init__(self):
        self.pool = ThreadPool()
        self.commands = list()

    def parallelize(self, sink: Sink, command: Command):
        arguments = [(sink, )]
        sink.collect(self.pool.starmap(command.do, arguments)[0])

    def do(self, sink: Sink):
        for command in self.commands:
            self.parallelize(sink, command)