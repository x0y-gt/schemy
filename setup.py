from setuptools import setup, find_packages

long_description = """A tool to auto-generate graqhQl types and models from a schema,
with a server included to makeit a graphQl API Server"""

setup(name='schemy',
      version='0.9.1',
      description='A graphQl server',
      long_description=long_description,
      keywords='graphql schema api python3',
      url='https://github.com/x0y-gt/schemy',
      author='Sebastian Godoy',
      author_email='sebas@milkyweb.co',
      license='GNUv3',
      packages=find_packages(),
      entry_points={
          'console_scripts': [
              'schemy = schemy.cmd.run:run'
          ]
      },
      install_requires=[
          'aiohttp==4.0.0a',
          'aiohttp-cors==0.7.0',
          'Click==7.0',
          'GraphQL-core-next>=1.0.3',
          'SQLAlchemy==1.3.4',
          'psycopg2-binary==2.8.2',
          'aiohttp-graphql@git+https://github.com/x0y-gt/aiohttp-graphql@use-core-next#egg=aiohttp-graphql-1.0',
          'alembic==1.0.10',
          'factory-boy==2.12',
          'spotlight==1.0.4',
          'python-dotenv==0.10.3',
          'slack-logger>=0.3.1',
      ],
      dependency_links=['git+https://github.com/x0y-gt/aiohttp-graphql@use-core-next#egg=aiohttp-graphql-1.0'],
      extras_require={
          'dev': [
              'pytest>=4.4.2',
              'pytest-runner',
              'aiohttp-devtools>=0.13.1',
          ]
      },
      setup_requires=["pytest-runner"],
      tests_require=["pytest"]
)
