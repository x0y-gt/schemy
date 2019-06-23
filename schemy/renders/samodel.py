from schemy.renders import BaseDatasource, SAColumn

__ALL__ = ['SAModel']

MODEL = """{imports}

__all__ = ['{name}Model']

class {name}Model(Base):
    __tablename__ = '{table}'\n
{cols}
    createdAt = Column(String, nullable=True)
    updatedAt = Column(String, nullable=True)

{rels}"""

class SAModel(BaseDatasource):

    def __init__(self, name):
        super(SAModel, self).__init__(name)
        self.imports = [
            'from api.model import Base',
        ]

    def render(self):
        cols = ''
        types = ['String']
        for col_name, col in self.cols.items():
            cols += col.render()
            types.append(col.type)

        rels = ''
        if self.rels:
            self.imports.append('from sqlalchemy.orm import relationship')
            for _rel_name, rel in self.rels.items():
                rels += rel.render()

        self.imports.append('from sqlalchemy import Column, ForeignKey, {types}'\
                        .format(types=", ".join(set(types))))
        code = MODEL.format(
            name=self.name,
            table=self.name.lower(),
            cols=cols,
            rels=rels,
            imports="\n".join(self.imports))
        return code
