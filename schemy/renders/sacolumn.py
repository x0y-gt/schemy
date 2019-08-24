from schemy.renders import Base

__ALL__ = ['SAColumn']

COLUMN = "    {name} = Column({type}{key}{nullable})\n{relationship}"
RELATIONSHIP = "    {name} = relationship('{model}'{backref}{uselist}{secondary})\n"

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
        self.__secondary = ''
        self.__relationship = False
        self.__uselist = False

    @property
    def pk(self):
        return self.__pk

    @pk.setter
    def pk(self, pk):
        self.__pk = bool(pk)

    @property
    def fk(self):
        return self.__fk

    @fk.setter
    def fk(self, fk: str):
        self.__fk = fk

    @property
    def backref(self):
        return self.__backref

    @backref.setter
    def backref(self, backref):
        self.__backref = backref

    @property
    def secondary(self):
        return self.__secondary

    @secondary.setter
    def secondary(self, secondary):
        self.__secondary = secondary

    @property
    def relationship(self):
        return self.__relationship

    @relationship.setter
    def relationship(self, relationship):
        self.__relationship = bool(relationship)

    @property
    def uselist(self):
        return self.__uselist

    @uselist.setter
    def uselist(self, uselist):
        self.__uselist = bool(uselist)

    @property
    def nullable(self):
        return self.__nullable

    @nullable.setter
    def nullable(self, nullable: bool = False):
        self.__nullable = nullable

    def render(self):
        code = ''
        # for many to one relationships
        if self.__relationship:
            backref = uselist = secondary = ''
            if self.__backref:
                backref = ', back_populates="%s"' % self.__backref
            #secondary flag is used to many to many relationships only
            if self.__secondary:
                secondary = ', secondary="%s"' % self.__secondary
            #uselist flag is used to one to one relationships only
            if self.__uselist:
                uselist = ', uselist=False'
            code = RELATIONSHIP.format(
                name=self.name,
                model=self.type+'Model',
                backref=backref,
                secondary=secondary,
                uselist=uselist
            )
        else:
            key = nullable = relationship = ''
            original_type = self.type

            if self.__pk:
                key = ', primary_key=True'
                self.type = 'Integer'

            # each foreign key must have its own relationship
            if self.__fk:
                key = (', ForeignKey("%s")' % (self.__fk)) + key
                backref = uselist = secondary = ''
                if self.__backref:
                    backref = ', back_populates="%s"' % self.__backref
                #this is a special case for link tables only
                if self.__pk and self.__fk and self.__backref:
                    backref = ', backref="%s"' % self.__backref
                relationship = RELATIONSHIP.format(
                    name=self.name,
                    model=original_type+'Model',
                    backref=backref,
                    secondary=secondary,
                    uselist=uselist
                )
                self.name += 'Id'
                self.type = 'Integer'

            if self.__nullable:
                nullable = ', nullable=True'

            code = COLUMN.format(
                name=self.name,
                type=self.type,
                key=key,
                nullable=nullable,
                relationship=relationship
            )

        return code
