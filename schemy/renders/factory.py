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

    def render(self, project_name='api'):
        imports = [
            'from datetime import datetime',
            'from random import randint',
            'import factory',
            'import PACKAGE_NAME.database.factories as factories',
            'from PACKAGE_NAME.model import datasource',
            'from PACKAGE_NAME.model import {name}Model'.format(name=self.name)
        ]

        cols = ''
        for _col_name, col in self.cols.items():
            cols += col.render()

        rels = ''
        if self.rels:
            for _rel_name, rel in self.rels.items():
                rels += rel.render()

        code = MODEL.format(
            name=self.name,
            cols=cols,
            rels=rels,
            imports="\n".join(imports))
        code = code.replace('PACKAGE_NAME', project_name)
        return code
