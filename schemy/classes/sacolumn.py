from schemy.classes.base import Base

__ALL__ = ['SAColumn']

COLUMN = "    {name} = Column({type}{key}{nullable})\n{relationship}"
RELATIONSHIP = "    {name} = relationship('{model}'{backref})\n"

class SAColumn(Base):
    """SqlAlchemy column, it works like a leaf class, it renders a class property in this case a model class column"""

    def __init__(self, name: str, type_:str):
        self.name = name
        self.type = type_
        if (name.lower()=='id'):
            self.__pk = True
        else:
            self.__pk = False
        self.__fk = ''
        self.__nullable = False
        self.__backref = ''
        self.__relationship = False

    @property
    def nullable(self):
        return self.__nullable

    @nullable.setter
    def nullable(self, nullable: bool = False):
        self.__nullable = nullable
        return self

    @property
    def fk(self):
        return self.__fk

    @fk.setter
    def fk(self, fk):
        self.__fk = bool(fk)
        return self

    @property
    def backref(self):
        return self.__backref

    @backref.setter
    def backref(self, backref):
        self.__backref = backref
        return self

    @property
    def relationship(self):
        return self.__relationship

    @relationship.setter
    def relationship(self, relationship):
        self.__relationship = bool(relationship)
        return self

    def render(self):
        code = ''
        # for many to one relationships
        if self.__relationship:
            code = RELATIONSHIP.format(name=self.name, model=self.type+'Model', backref='')
        else:
            key = nullable = relationship = ''
            type_ = self.type

            if self.__pk:
                key = ', primary_key=True'
            # each foreign key must have its own relationship
            elif self.__fk:
                key = ', ForeignKey("%s")' % (self.type.lower()+'.id')
                backref = ''
                if self.backref:
                    backref = ', back_populates="%s"' % self.__backref
                relationship = RELATIONSHIP.format(name=self.name, model=self.type+'Model', backref=backref)
                self.name += 'Id'
                type_ = 'Integer'

            if self.__nullable:
                nullable = ', nullable=True'
            code = COLUMN.format(name=self.name, type=type_, key=key, nullable=nullable, relationship=relationship)

        return code
