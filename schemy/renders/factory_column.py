from schemy.renders import Base

__all__ = ['FactoryColumn']


COLUMN = "    {name} = {factory}\n"

class FactoryColumn(Base):
    """Renders a factory column, it works like a leaf class, it renders a class
    property"""

    def __init__(self, name:str, gql_type:str = None):
        self.name = name
        self.__gql_type = gql_type
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
            provider = self._set_faker_provider()
            factory = "factory.Faker('{provider}')".format(provider=provider)

        code = COLUMN.format(name=self.name, factory=factory)

        return code

    def _set_faker_provider(self):
        """Give the property name, returns an appropiate faker provider"""
        if self.__gql_type == 'Int' or self.__gql_type == 'ID':
            return 'pyint'
        elif self.__gql_type == 'Float':
            return 'pyfloat'
        elif self.__gql_type == 'Boolean':
            return 'pybool'
        else:
            # special cases
            if 'name' in self.name:
                return 'name'
            elif 'email' in self.name:
                return 'email'
            elif 'phone' in self.name:
                return 'phone_number'
            else:
                return 'text'
