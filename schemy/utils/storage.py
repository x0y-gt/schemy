__ALL__ = ['Storage']

class Storage():

    """Docstring for Storage. """

    def __init__(self, path, mode='r'):
        self.__path = path
        self.__mode = mode
        self.__file = None
        self.__content = ''
        self.__readed = False

    def open(self, path: str = '', mode=''):
        if not mode:
            mode = self.__mode
        if not path:
            path = self.__path
        self.__file = open(path, mode)

    def close(self):
        self.__file.close()

    @property
    def content(self):
        if not self.__readed:
            self.__content = self.__file.read()
            self.__readed = True
        return self.__content

    @content.setter
    def content(self, content:str):
        self.__content = content
        self.__file.write(self.__content)
        return self.__content

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, type, val, tb):
        self.close()
