from schemy.renders import BaseDatasource

__ALL__ = ['Factory']

MODEL = """{imports}

__all__ = ['{name}Factory']

class {name}Factory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta(object):
        model = {name}Model
        sqlalchemy_session = datasource.session

{cols}
    createdAt = factory.LazyFunction(datetime.now)
    updatedAt = factory.LazyFunction(datetime.now)

{rels}"""

class Factory(BaseDatasource):

    def __init__(self, name):
        super(Factory, self).__init__(name)

    def render(self):
        imports = [
            'from datetime import datetime',
            'from random import randint',
            'import factory',
            'from api.model import datasource',
        ]
        imports.append('from api.model import {name}Model'.format(
            name=self.name
        ))

        cols = ''
        for _col_name, col in self.cols.items():
            #this is an exception to columns in many to many tables
            if col.many_to_one:
                imports.append('from .{module} import {name}Factory'.format(
                    module=col.many_to_one.lower(),
                    name=col.many_to_one
                ))
            cols += col.render()

        rels = ''
        if self.rels:
            for _rel_name, rel in self.rels.items():
                if rel.many_to_one:
                    imports.append('from .{module} import {name}Factory'.format(
                        module=rel.many_to_one.lower(),
                        name=rel.many_to_one
                    ))
                rels += rel.render()

        code = MODEL.format(
            name=self.name,
            cols=cols,
            rels=rels,
            imports="\n".join(imports))
        return code
