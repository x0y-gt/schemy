from schemy.classes.base import BaseModel
from schemy.classes.sacolumn import SAColumn

__ALL__ = ['SAModel']

MODEL = """{imports}

__ALL__ = ['{name}Model']

class {name}Model(Base, Model):
    __tablename__ = '{table}'\n
{cols}
    createdAt = Column(String, nullable=True)
    updatedAt = Column(String, nullable=True)

{rels}"""

class SAModel(BaseModel):

    def __init__(self, name):
        super(SAModel, self).__init__(name)

    def render(self):
        imports = ['from api.model import Base, Model']

        cols = ''
        types = []
        for col_name, col in self.cols.items():
            cols += col.render()
            types.append(col.type)

        rels = ''
        if (len(self.rels)):
            imports.append('from sqlalchemy import Column, ForeignKey, {types}'.format(types=", ".join(types)))
            imports.append('from sqlalchemy.orm import relationship')
            for rel_name, rel in self.rels.items():
                rels += rel.render()

        code = MODEL.format(
            name=self.name,
            table=self.name.lower(),
            cols=cols,
            rels=rels,
            imports="\n".join(imports))
        return code
