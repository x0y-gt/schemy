import pytest
from schemy.graphql.schema import Schema
from graphql import GraphQLSchema

SCHEMA_PATH = '../tests/schema.sdl'

def test_schema_loading():
    schema = Schema(SCHEMA_PATH)
    assert type(schema.load()) is GraphQLSchema

def test_map_schema_types():
    schema = Schema(SCHEMA_PATH)
    res = {
        'enums': {},
        'objects': {'Author': {'field': {'id': {'nullable': False, 'type': 'ID'},
                                      'name': {'nullable': False,
                                               'type': 'String'}},
                            'relationship': {'books': {'list': True,
                                                       'nullable': False,
                                                       'type': 'Book'}}},
                 'Book': {'field': {'id': {'nullable': False, 'type': 'ID'},
                                    'name': {'nullable': False, 'type': 'String'}},
                          'relationship': {'authors': {'list': True,
                                                       'nullable': True,
                                                       'type': 'Author'},
                                           'publisher': {'list': False,
                                                         'nullable': True,
                                                         'type': 'Publisher'}}},
                 'Publisher': {'field': {'id': {'nullable': False, 'type': 'ID'},
                                         'name': {'nullable': False,
                                                  'type': 'String'}},
                               'relationship': {'books': {'list': True,
                                                          'nullable': True,
                                                          'type': 'Book'}}}
        }
    }
    assert schema.map_types() == res
