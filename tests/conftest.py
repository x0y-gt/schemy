import pytest

@pytest.fixture
def schema_default():
    """Creates an Schema instance using the default schema definition"""
    from schemy.graphql.schema import Schema
    SCHEMA_PATH = '../tests/schema_books.sdl'
    return Schema(SCHEMA_PATH)

