from schemy import Schemy

from api import config
from api.model import datasource

sdl_path = config.get('APP_ROOT_DIR') + config.get('APP_SDL_PATH')
schemy = Schemy(sdl_path)
schemy.types_path = config.get('APP_TYPES_DIR')
schemy.datasource = datasource
schemy.build()


query = """{
    book(id: "1") {
        name
    }
}"""
print(schemy.handle(query))
