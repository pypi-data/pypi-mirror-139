import abc

class Sink(abc.ABC):

    @abc.abstractproperty
    def data(self):
        pass

    @abc.abstractmethod
    def collect(self, data):
        pass