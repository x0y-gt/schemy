import os
from aiohttp import web
from aiohttp_graphql import GraphQLView
import aiohttp_cors
from schemy import Schemy

from {project_name} import config
from {project_name}.model import datasource

gqlv = None

def bootstrap_schemy():
    sdl_path = config.get('APP_ROOT_DIR') + config.get('APP_SDL_PATH')
    schemy = Schemy(sdl_path)
    schemy.types_path = config.get('APP_TYPES_DIR')
    schemy.datasource = datasource
    schemy.build()
    return schemy

async def handler(request):
    global gqlv

    return await gqlv(request)

def get_app():
    global gqlv

    schemy = bootstrap_schemy()
    app = web.Application()

    # configure app
    gqlv = GraphQLView(
        schema=schemy.schema(),
        field_resolver=schemy.get_resolver(),
        batch=True,
        graphiql=True
    )

    get_route = app.router.add_route('GET', '/graphql', handler, name='graphql')
    post_route = app.router.add_route('POST', '/graphql', handler, name='graphql')

    #enable CORS
    cors = aiohttp_cors.setup(app, defaults={
        "*": aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            expose_headers=("X-Custom-Server-Header",),
            allow_headers=("X-Requested-With", "Content-Type"),
            max_age=3600,
        )
    })
    cors.add(get_route)
    cors.add(post_route)

    return app

if __name__ == '__main__':
    web.run_app(get_app(), port=os.getenv('APP_PORT'))
