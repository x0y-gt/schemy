from schemy.classes.base import BaseModel
from schemy.classes.sacolumn import SAColumn

__ALL__ = ['SAModel']

MODEL = """{imports}

__ALL__ = ['{name}Model']

class {name}Model(Base, Model):
    __tablename__ = '{table}'\n
{cols}
{rels}"""

class SAModel(BaseModel):

    def __init__(self, name):
        super(SAModel, self).__init__(name)

    def render(self):
        #cols = relationships = ''
        #types = []
        #imports = ['from api.model import Base, Model']
        #importRelationship = False

        cols = ''
        for col_name, col in self.cols.items():
            cols += col.render()

        rels = ''
        for rel_name, rel in self.rels.items():
            rels += rel.render()
        #    if Attr.type not in types:
        #        types.append(Attr.type)
        #    # verify if a model match to add backref in the relationship
        #    if Attr.fk and Attr.fk in self.backrefs.keys():
        #        importRelationship = True
        #        Attr.set_backref(self.backrefs[Attr.fk])
        #    cols += Attr.render()
        #imports.append('from sqlalchemy import Column, ForeignKey, {types}'.format(types=", ".join(types)))

        #if len(self.relationships):
        #    importRelationship = True
        #    for rel in self.relationships:
        #        relationships += '    {field} = relationship("{model}")'.format(field=rel['field'].lower(), model=rel['model']+'Model')
        #    relationships = "\n" + relationships

        #if importRelationship:
        #    imports.append('from sqlalchemy.orm import relationship')

        code = MODEL.format(
            name=self.name,
            table=self.name.lower(),
            cols=cols,
            rels=rels,
            imports="\n")
        return code
