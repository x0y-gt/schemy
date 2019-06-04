from abc import ABC

__all__ = ['BaseType']


class BaseType(ABC):
    def __new__(cls, *args, **kwargs):
        instance = super(BaseType, cls).__new__(cls, *args, **kwargs)
        if hasattr(instance, 'DATASOURCE'):
            instance._model = instance.DATASOURCE()
            instance._query = instance.model.query()
        return instance

    def query(self):
        return self._query if self._query else None

    def model(self):
        return self._model if self._model else None
