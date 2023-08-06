from .Sink import Sink

class ConcreteSink(Sink):

    @property
    def data(self):
        return self._data

    def collect(self, data):
        self._data = data