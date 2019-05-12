import pytest
from graphql import GraphQLSchema

def test_schema_loading(schema_default):
    assert type(schema_default.load()) is GraphQLSchema

def test_map_schema_types(schema_default):
    assert schema_default.map_types() == {
        'enums': {},
        'objects': {
            'Author': {
                'field': {
                    'id': {
                        'nullable': False,
                        'type': 'ID'
                    },
                    'name': {
                        'nullable': False,
                        'type': 'String'
                    }
                },
                'relationship': {
                    'books': {
                        'list': True,
                        'nullable': False,
                        'type': 'Book'
                    }
                }
            },
            'Book': {
                'field': {
                    'id': {
                        'nullable': False,
                        'type': 'ID'
                    },
                    'name': {
                        'nullable': False,
                        'type': 'String'
                    }
                },
                'relationship': {
                    'authors': {
                        'list': True,
                        'nullable': True,
                        'type': 'Author'
                    },
                    'publisher': {
                        'list': False,
                        'nullable': True,
                        'type': 'Publisher'
                    }
                }
            },
            'Publisher': {
                'field': {
                    'id': {
                        'nullable': False,
                        'type': 'ID'
                    },
                    'name': {
                        'nullable': False,
                        'type': 'String'
                    }
                },
                'relationship': {
                    'books': {
                        'list': True,
                        'nullable': True,
                        'type': 'Book'
                    }
                }
            }
        }
    }
