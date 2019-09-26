# Schemy

It is a Schema-Driven development tool to generate GraphQl APIs from a GraphQl Schema using python. It has its own server

## Install

`schemy new-project NAME`

## Bootstraping A Project

After checking database config

```
schemy sync-models
schemy sync-types
python setup.py develop ???
alembic revision --autogenerate -m "First migration, defining entities"
alembic upgrade head
schemy sync-factories
schemy seed
```
## Running

`python api/app.py`

## Deploying to Prod

Using docker-machine

`COMPOSE_TLS_VERSION=TLSv1_2 docker-compose -f docker/docker-composer.yaml -f docker/docker-composer.prod.yaml up -d`
