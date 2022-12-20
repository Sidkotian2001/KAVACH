from abc import (ABC, abstractmethod)

class Model(ABC):
    @abstractmethod
    def __init__(self):
        pass
    @abstractmethod
    def create_model(self):
        pass
    @abstractmethod
    def prediction(self):
        pass

class Image(ABC):
    @abstractmethod
    def show_image(self):
        pass
    @abstractmethod
    def preprocess_image(self):
        pass