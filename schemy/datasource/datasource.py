from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from schemy.utils import Singleton


class Datasource(metaclass=Singleton):

    def __init__(self, db_connection):
        """This class is a global singleton to manage global settings
        to access data
        """
        # DB connection
        engine = create_engine(db_connection, echo=True)
        self.__data = {
            'connection_string': db_connection,
            'engine': engine,
            'session': scoped_session(sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=engine
            ))
        }

    @property
    def session(self):
        return self.__data['session']
