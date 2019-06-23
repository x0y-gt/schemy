from abc import ABC, abstractmethod

__ALL__ = ['Base']

class Base(ABC):
    """Base class that defines how to render another code class like a sqlalchemy model class"""
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def render(self):
        """Return the rendered code of the class and its childs"""
        pass
