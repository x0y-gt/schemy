__ALL__ = ['Storage']

class Storage():

    """Docstring for Storage. """

    def __init__(self, path):
        self.__path = path
        self.__file = None
        self.__content = None

    def open(self, path:str = ''):
        if not path:
            path = self.__path
        self.__file = open(path, 'w')

    def close(self):
        self.__file.close()

    @property
    def content(self):
        return self.__content

    @content.setter
    def content(self, content:str):
        self.__content = content
        self.__file.write(self.content)
        return self.__content

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, type, val, tb):
        self.close()
