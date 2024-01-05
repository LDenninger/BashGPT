from abc import abstractmethod


class ModelInterface(object):

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def __call__(self):
        pass