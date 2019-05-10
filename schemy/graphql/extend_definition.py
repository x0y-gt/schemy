from graphql import is_list_type, is_non_null_type, is_wrapping_type

__ALL__ = ['contains_list_type', 'contains_non_null_type', 'get_list_type']

def contains_non_null_type(type_):
    if type_:
        while is_wrapping_type(type_):
            if is_non_null_type(type_):
                return True
            type_ = type_.of_type
    return False

def get_list_type(type_):
    if type_:
        while is_wrapping_type(type_):
            if is_list_type(type_):
                return type_
            type_ = type_.of_type
    return None

def contains_list_type(type_):
    """Return true if contains a list type"""
    return bool(get_list_type(type_))
