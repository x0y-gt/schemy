from {project_name}.model import datasource
import {project_name}.database.factories as factories

def seed():
    factories.init()
    pass

if __name__ == '__main__':
    seed()
