from setuptools import setup, find_packages

long_description = """An API based in schemy"""

setup(name='{project_name}',
      version='1.0',
      description='A graphQl API',
      long_description=long_description,
      keywords='graphql schema api python3',
      url='',
      author='',
      author_email='',
      license='GNUv3',
      packages=find_packages(),
      install_requires=[
          'schemy',
      ],
      extras_require={
          'dev': [
              'alembic==1.0.10',
              'factory-boy',
              'pytest>=4.4.2',
              'pytest-runner',
          ]
      },
      setup_requires=["pytest-runner"],
      tests_require=["pytest"]
)
