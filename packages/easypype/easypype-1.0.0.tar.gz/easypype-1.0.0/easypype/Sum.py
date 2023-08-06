from .Command import Command
from .Sink import Sink

class Sum(Command):

    def __init__(self, amount):
        self.amount = amount

    def sum(self, sink: Sink):
        return [i + self.amount for i in sink.data]

    def do(self, sink: Sink):
        return self.sum(sink)