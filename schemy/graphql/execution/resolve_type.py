from graphql.type.definition import get_named_type, GraphQLScalarType

def field_resolver(cls, root, info, **args):
    return_type = get_named_type(info.return_type)
    # if return type is scalar then resolve with default resolver
    if isinstance(return_type, GraphQLScalarType):
        return default_field_resolver(root, info, **args)

    type_name = info.return_type.name
    # instantiate the type
    new_type = getattr(Types, type_name)
    type_ = new_type()

    # Look for same field name as defined in the Query root object
    if info.parent_type.name == 'Query':
        prefix = 'resolve_'
        field_name = '{prefix}{name}'.format(prefix=prefix, name=info.field_name)
    else:
        prefix = 'resolve_type_'
        field_name = '{prefix}{name}'.format(prefix=prefix, name=info.parent_type.name.lower())

    # find and execute the resolver
    if hasattr(type_, field_name):
        query_resolver = getattr(type_, field_name)
        if info.parent_type.name == 'Query':
            return query_resolver(**args)
        else:
            return query_resolver(root, **args)
    else:
        print('log.warning: resolver {type_name}.{field_name} not found'.format(type_name=type_name, field_name=field_name))

    return None
