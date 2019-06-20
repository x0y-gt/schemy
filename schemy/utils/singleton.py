__all__ = [
    'Singleton'
]

class Singleton(type):
    """Base singleton declaration
    Another class can become a singleton by inheriting this class"""
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            # now the type's __call__() is only executed if cls is not in cls._instances
            # This way we prevent new objects from being created if one exists
            #when the constructor of classes deriving from MetaSingleton are created
            cls._instances[cls] = super().__call__(*args, **kwargs)

        return cls._instances[cls]
