from abc import ABC

__all__ = ['BaseType']


class BaseType(ABC):
    """This abstract class is the parent of the type's classes
    It helps to access the query object to do the queries from the type classes"""

    def __new__(cls, datasource, *args, **kwargs):
        instance = super(BaseType, cls).__new__(cls, *args, **kwargs)
        if hasattr(instance, 'DATASOURCE'):
            instance._session = datasource.session
            instance._query = None
            if (instance.DATASOURCE):
                instance._query = datasource.session.query(instance.DATASOURCE)
        return instance

    def query(self):
        return self._query if self._query else None

    def session(self):
        return self._session if self._session else None
