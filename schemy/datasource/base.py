__all__ = [
    'BaseModel'
]

class BaseModel():
    @classmethod
    def query(cls):
        return db_session.query(cls)

    def getSession():
        return db_session
