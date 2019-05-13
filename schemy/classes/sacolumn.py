from schemy.classes.base import Base

__ALL__ = ['SAColumn']

COLUMN = "    {name} = Column({type}{key}{nullable})\n"
RELATIONSHIP = "    {name} = relationship('{model}')"

class SAColumn(Base):
    """SqlAlchemy column, it works like a leaf class, it renders a class property in this case a model class column"""

    def __init__(self, name: str):
        self.name = name
        self.type = 'String'
        if (name.lower()=='id'):
            self.pk = True
        else:
            self.pk = False
        self.fk = None
        self.nullable = False
        self.backref = ''
        self.relationship = False

    def set_nullable(self, nullable: bool = False):
        self.nullable = nullable

    def set_type(self, type_):
        self.type = type_

    def set_fk(self, fk: bool = True):
        self.fk = fk

    def set_backref(self, backref):
        self.backref = backref

    def set_relationship(self, relationship: bool = True):
        self.relationship = relationship

    def render(self):
        code = ''
        if self.relationship:
            code = RELATIONSHIP.format(name=self.name, model=self.type+'Model')
        else:
            key = nullable = ''

            if self.pk:
                key = ', primary_key=True'
            elif self.fk:
                key = ', ForeignKey("%s")' % (self.fk.lower()+'.id')
                backref = ''
                if self.backref:
                    backref = ', back_populates="%s"' % self.backref
                relationship = '    {field} = relationship("{model}"{backref})\n'.format(field=self.name, model=self.fk+'Model', backref=backref)
                self.name += 'Id'

            if self.nullable:
                nullable = ', nullable=True'
            code = COLUMN.format(name=self.name, type=self.type, key=key, nullable=nullable)

        return code
