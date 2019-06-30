from aiohttp import web
from aiohttp_graphql import GraphQLView
from schemy import Schemy

from api import config
from api.model import datasource


def bootstrap_schemy():
    sdl_path = config.get('APP_ROOT_DIR') + config.get('APP_SDL_PATH')
    schemy = Schemy(sdl_path)
    schemy.types_path = config.get('APP_TYPES_DIR')
    schemy.datasource = datasource
    schemy.build()
    return schemy

if __name__ == '__main__':
    schemy = bootstrap_schemy()

    app = web.Application()
    # configure app
    gql_view = GraphQLView(
        schema=schemy.schema(),
        field_resolver=schemy.get_resolver(),
        graphiql=True
    )
    app.router.add_route('GET', '/graphql', gql_view, name='graphql')
    app.router.add_route('POST', '/graphql', gql_view, name='graphql')

    web.run_app(app, port=8080)
