from setuptools import setup, find_packages

setup(name='schemy',
      version='0.1',
      description='A graphQl server',
      long_description='A tool to auto-generate graqhQl types and models from a schema, with a server included to makeit a graphQl API Server',
      keywords='graphql schema api python3',
      url='https://github.com/x0y-gt/schemy',
      author='Sebastian Godoy',
      author_email='sebas@milkyweb.co',
      license='GNUv3',
      packages=find_packages(),
      install_requires=[
          'Click==7.0',
          'GraphQL-core-next>=1.0.3',
          'SQLAlchemy==1.3.4',
          'psycopg2-binary==2.8.2'
      ],
      extras_require={
          'dev': [
              'alembic==1.0.10',
              'pytest>=4.4.2',
              'pytest-runner'
          ]
      },
      setup_requires=["pytest-runner"],
      tests_require=["pytest"]
)
