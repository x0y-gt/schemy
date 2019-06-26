from schemy.renders import Base

__all__ = ['FactoryColumn']

COLUMN = "    {name} = {factory}\n"

class FactoryColumn(Base):
    """Renders a factory column, it works like a leaf class, it renders a class
    property"""

    def __init__(self, name: str):
        self.name = name
        if name.lower() == 'id':
            self.__pk = True
        else:
            self.__pk = False
        self.__one_to_many = None
        self.__many_to_one = None
        self.__backref = ''

    @property
    def pk(self):
        return self.__pk

    @pk.setter
    def pk(self, pk):
        self.__pk = bool(pk)

    @property
    def one_to_many(self):
        return self.__one_to_many

    @one_to_many.setter
    def one_to_many(self, one_to_many: str):
        self.__one_to_many = one_to_many

    @property
    def many_to_one(self):
        return self.__many_to_one

    @many_to_one.setter
    def many_to_one(self, many_to_one: str):
        self.__many_to_one = many_to_one

    @property
    def backref(self):
        return self.__backref

    @backref.setter
    def backref(self, backref):
        self.__backref = backref

    def render(self):
        code = ''
        factory = ''

        if self.__pk:
            factory = 'factory.Sequence(lambda n: n+1)'
        elif self.__one_to_many:
            factory = "factory.RelatedFactoryList('{one_to_many}', '{backref}'"\
                        ", size=lambda: randint(0,3))".format(
                            one_to_many=self.__one_to_many,
                            backref=self.__backref
                        )
        elif self.__many_to_one:
            factory = "factory.SubFactory({factory}{backref})".format(
                factory=self.__many_to_one + 'Factory',
                backref=', ' + self.__backref if self.__backref else ''
            )
        else:
            factory = "factory.Faker('{name}')".format(name=self.name)

        code = COLUMN.format(name=self.name, factory=factory)

        return code
