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
          'GraphQL-core-next>=1.0.3'
      ],
      extras_require={
          'dev': [
              'pytest>=4.4.2'
          ]
      }
)
