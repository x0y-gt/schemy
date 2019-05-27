from graphql import is_scalar_type, is_enum_type, is_object_type, get_named_type
from schemy.graphql.type.definition import contains_non_null_type, contains_list_type, get_list_type

__all__ = ['map_schema_types']

def map_schema_types(schema, ignore=['Query', 'Mutation']):
    """Iterate over a graphQl schema to get the schema types and its relations

    The process ignores the root types like Query and Mutation and the Scalar types"""
    objects = dict()
    enums = dict()
    for type_name, type_obj in schema.type_map.items():
        # Iterating over all the items of the schema
        # Ignore internal types and root types
        if (type_name[:2]!='__') and (type_name not in ignore):
            # ENUM types
            if is_enum_type(type_obj):
                enums[type_name] = [] # values
            # Graphql Types
            elif is_object_type(type_obj):
                #Create the type obj
                obj = _get_object(objects, type_name)

                # Iterate over all fields of the graphql type
                for field_name, field_obj in type_obj.fields.items():
                    field = get_named_type(field_obj.type) # Returns a scalar or an object
                    # setting non null
                    nullable = True
                    if contains_non_null_type(field_obj.type):
                        nullable = False

                    if is_scalar_type(field):
                        obj['field'][field_name] = {'type':field.name, 'nullable': nullable}
                    elif is_object_type(field):
                        # if it's a list of types, that means that I'm the parent in a one to many relationship
                        list_ = False
                        if contains_list_type(field_obj.type):
                            list_ = True
                        obj['relationship'][field_name] = {'type': field.name, 'nullable': nullable, 'list': list_}

    return {'objects':objects, 'enums':enums}

def _get_object(objects, obj_name):
    """Return a object, it's created if it doesn't exists"""
    if obj_name not in objects:
        obj = {'field': {}, 'relationship': {}}
        objects[obj_name] = obj
    else:
        obj = objects[obj_name]
    return obj
