import pytest
from schemy.schema import Schema
from graphql import GraphQLSchema

SCHEMA_PATH = '../tests/schema.sdl'

def test_schema_loading():
    schema = Schema(SCHEMA_PATH)
    assert type(schema.load()) is GraphQLSchema
