from schemy.renders import Base

__all__ = ['FactoryColumn']



class FactoryColumn(Base):
    """Renders a factory column, it works like a leaf class, it renders a class
    property"""

    COLUMN = "    {name} = {factory}\n"

    def __init__(self, name:str, gql_type:str = None):
        self.name = name
        self.__gql_type = gql_type
        if name.lower() == 'id':
            self.__pk = True
        else:
            self.__pk = False
        self.__one_to_many = None
        self.__many_to_one = None
        self.__many_to_many = None
        self.__one_to_one = None
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
    def many_to_many(self):
        return self.__many_to_many

    @many_to_many.setter
    def many_to_many(self, many_to_many: str):
        self.__many_to_many = many_to_many

    @property
    def one_to_one(self):
        return self.__one_to_one

    @one_to_one.setter
    def one_to_one(self, one_to_one: str):
        self.__one_to_one = one_to_one

    @property
    def backref(self):
        return self.__backref

    @backref.setter
    def backref(self, backref):
        self.__backref = backref

    def _render_many2one(self):
        code = """
    @factory.post_generation
    def {field_name}(self, create, extracted): #pylint: disable=method-hidden
        \"\"\"many to one relationship\"\"\"
        if not create:
            return None

        #adding me to the stack
        if '{type}' not in factories.stack:
            factories.stack['{type}'] = []
            factories.stack['_owner']['{type}'] = []
        if self not in factories.stack['{type}']:
            factories.stack['{type}'].append(self)

        obj = None
        if extracted:
            obj = extracted
        elif '{resolved_type}' in factories.stack and '{resolved_type}' not in factories.stack['_owner']['{type}']:
            #looks for the lastest created if any
            obj = factories.stack['{resolved_type}'][-1]
        else:
            from PACKAGE_NAME.database.factories.{resolved_type_lower} import {resolved_type}Factory
            obj = {resolved_type}Factory.create({resolved_type_field_name}=[self])

        self.{field_name} = obj
        return obj
"""
        return code.format(
            field_name=self.name,
            type=self.__gql_type,
            resolved_type=self.__many_to_one,
            resolved_type_lower=self.__many_to_one.lower(),
            resolved_type_field_name=self.__backref
        )

    def _render_one2many(self):
        code = """
    @factory.post_generation
    def {field_name}(self, create, extracted): #pylint: disable=method-hidden
        \"\"\"one to many relationship\"\"\"
        if not create:
            return None

        #adding me to the factories.stack
        if '{type}' not in factories.stack:
            factories.stack['{type}'] = []
            factories.stack['_owner']['{type}'] = []
        if self not in factories.stack['{type}']:
            factories.stack['{type}'].append(self)

        objs = []
        if extracted:
            objs = extracted
        elif '{resolved_type}' in factories.stack and '{resolved_type}' not in factories.stack['_owner']['{type}']:
            #looks for the lastest created if any
            objs = [factories.stack['{resolved_type}'][-1]]
        else:
            #create it if they does not exists
            from PACKAGE_NAME.database.factories.{resolved_type_lower} import {resolved_type}Factory
            for _ in range(randint(1, 3)):
                obj = {resolved_type}Factory.create({resolved_type_field_name}=self)
                objs.append(obj)

        self.{field_name}.extend(objs) #pylint: disable=no-member
        return objs
"""
        return code.format(
            field_name=self.name,
            type=self.__gql_type,
            resolved_type=self.__one_to_many,
            resolved_type_lower=self.__one_to_many.lower(),
            resolved_type_field_name=self.__backref
        )

    def _render_many2many(self):
        code = """
    @factory.post_generation
    def {field_name}(self, create, extracted):
        \"\"\"many to many relationship\"\"\"
        if not create:
            return None

        #adding me to the factories.stack
        if '{type}' not in factories.stack:
            factories.stack['{type}'] = []
            factories.stack['_owner']['{type}'] = []
        if self not in factories.stack['{type}']:
            factories.stack['{type}'].append(self)

        objs = []
        if extracted:
            objs = extracted
        elif '{resolved_type}' in factories.stack and '{resolved_type}' not in factories.stack['_owner']['{type}']:
            #looks for the lastest created if any
            objs = set([obj for obj in factories.stack['{resolved_type}'] if self not in obj.{resolved_type_field_name}])
            #objs[0].{resolved_type_field_name}.extend([self])
            if objs:
                self.{field_name}.extend(list(objs)) #pylint: disable=no-member
        else:
            #create ours if they does not exists
            #add me as owner
            factories.stack['_owner']['{type}'].append('{resolved_type}')
            from PACKAGE_NAME.database.factories.{resolved_type_lower} import {resolved_type}Factory
            for _ in range(randint(1, 3)):
                obj = {resolved_type}Factory.create({resolved_type_field_name}=[self])
                objs.append(obj)
            self.{field_name}.extend(objs) #pylint: disable=no-member

        return objs
"""
        return code.format(
            field_name=self.name,
            type=self.__gql_type,
            resolved_type=self.__many_to_many,
            resolved_type_lower=self.__many_to_many.lower(),
            resolved_type_field_name=self.__backref
        )

    def _render_one2one(self):
        code = """
    @factory.post_generation
    def {field_name}(self, create, extracted): #pylint: disable=method-hidden
        \"\"\"many to one relationship\"\"\"
        if not create:
            return None

        #adding me to the stack
        if '{type}' not in factories.stack:
            factories.stack['{type}'] = []
            factories.stack['_owner']['{type}'] = []
        if self not in factories.stack['Seller']:
            factories.stack['{type}'].append(self)

        obj = None
        if extracted:
            obj = extracted
        elif '{resolved_type}' in factories.stack and '{resolved_type}' not in factories.stack['_owner']['{type}']:
            #looks for the lastest created if any
            obj = factories.stack['{resolved_type}'][-1]
        else:
            from PACKAGE_NAME.database.factories.{resolved_type_lower} import {resolved_type}Factory
            obj = {resolved_type}Factory.create({resolved_type_field_name}=self)

        self.{field_name} = obj
        return obj
"""
        return code.format(
            field_name=self.name,
            type=self.__gql_type,
            resolved_type=self.__one_to_one,
            resolved_type_lower=self.__one_to_one.lower(),
            resolved_type_field_name=self.__backref
        )


    def render(self):
        code = ''
        factory = ''

        if self.__pk:
            factory = 'factory.Sequence(lambda n: n+1)'
            code = self.COLUMN.format(name=self.name, factory=factory)
        elif self.__one_to_many:
            code = self._render_one2many()
        elif self.__many_to_one:
            code = self._render_many2one()
        elif self.__many_to_many:
            code = self._render_many2many()
        elif self.__one_to_one:
            code = self._render_one2one()
        else:
            # probably it's a scalar not a relationship
            provider = self._grahql2factoryboy()
            factory = "factory.Faker('{provider}')".format(provider=provider)
            code = self.COLUMN.format(name=self.name, factory=factory)

        return code

    def _grahql2factoryboy(self):
        """Give the property name, returns an appropiate faker provider"""
        new_type = 'text'

        if self.__gql_type == 'Int' or self.__gql_type == 'ID':
            new_type = 'pyint'
        if self.__gql_type == 'Float':
            new_type = 'pyfloat'
        if self.__gql_type == 'Boolean':
            new_type = 'pybool'

        # special cases
        if 'name' in self.name:
            new_type = 'name'
        if 'email' in self.name:
            new_type = 'email'
        if 'phone' in self.name:
            new_type = 'phone_number'

        return new_type
