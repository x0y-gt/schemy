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

class BaseModel(Base):
    """Definition of a base model class"""

    def __init__(self, name):
        super(BaseModel, self).__init__(name)
        self.cols = {}
        self.rels = {}

    def add_column(self, col: Base):
        self.cols[col.name] = col
        return self

    def del_column(self, name):
        if name in self.cols:
            del self.cols[name]
        return self

    def add_relationship(self, col: Base):
        self.rels[col.name] = col
        return self

    def del_relationship(self, name):
        if name in self.rels:
            del self.rels[name]
        return self
