__ALL__ = ['gql2alchemy']

def gql2alchemy(gql_type):
    gql_type = gql_type.title()
    if (gql_type in ['Id', 'Int']):
        return 'Integer'
    else:
        return gql_type
