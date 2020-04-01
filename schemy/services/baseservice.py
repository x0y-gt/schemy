from abc import ABC
from schemy.datasources import Datasource

__all__ = ['BaseService']


class BaseService(ABC):
    """This abstract class is the parent of the service's classes
    It helps to access the query object to do the queries from the service classes"""

    def __new__(cls, *args, **kwargs):
        instance = super(BaseService, cls).__new__(cls, *args, **kwargs)
        if hasattr(instance, 'DATASOURCE'):
            instance._session = Datasource().session
            instance._query = None
            if (instance.DATASOURCE):
                instance._query = Datasource().session.query(instance.DATASOURCE)
        return instance

    def query(self):
        return self._query if self._query else None

    def session(self):
        return self._session if self._session else None
