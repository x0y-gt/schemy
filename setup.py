from setuptools import setup, find_packages

long_description = """A tool to auto-generate graqhQl types and models from a schema,
with a server included to makeit a graphQl API Server"""

setup(name='schemy',
      version='0.3',
      description='A graphQl server',
      long_description=long_description,
      keywords='graphql schema api python3',
      url='https://github.com/x0y-gt/schemy',
      author='Sebastian Godoy',
      author_email='sebas@milkyweb.co',
      license='GNUv3',
      packages=find_packages(),
      install_requires=[
          'asyncio',
          'aiohttp>=4.0.0a',
          'Click==7.0',
          'GraphQL-core-next>=1.0.3',
          'SQLAlchemy==1.3.4',
          'psycopg2-binary==2.8.2',
          'aiohttp-graphql'#@https://github.com/x0y-gt/aiohttp-graphql/tree/use-core-next#egg=aiohttp-graphql-1.0',
      ],
      extras_require={
          'dev': [
              'alembic==1.0.10',
              'factory-boy',
              'pytest>=4.4.2',
              'pytest-runner',
          ]
      },
      dependency_links=[
          'git+https://github.com/x0y-gt/aiohttp-graphql@use-core-next#egg=aiohttp-graphql-1.0',
      ],
      setup_requires=["pytest-runner"],
      tests_require=["pytest"]
)
