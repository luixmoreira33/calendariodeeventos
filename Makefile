#!/bin/bash
.PHONY: default help migrate migrations superuser service-port
.SILENT:

default: help

help:
	@echo "Usage:"
	@echo "  make build            - Construir containers para o ambiente local"
	@echo "  make migrate          - Executar migrações no banco de dados"
	@echo "  make migrations       - Criar novas migrações com base nas alterações do modelo"
	@echo "  make superuser        - Criar um superusuário"
	@echo "  make service-port     - Executar o serviço com portas abertas"

_local_env:
	-cp -n sample.env .env

build:
	docker-compose -f docker-compose.yml build --force-rm --no-cache --pull

build-local:
	docker-compose -f docker-compose-local.yml build --force-rm --no-cache --pull

up:
	docker-compose -f docker-compose.yml up -d

up-local:
	docker-compose -f docker-compose-local.yml up

down:
	docker-compose -f docker-compose.yml down

down-local:
	docker-compose -f docker-compose-local.yml down

migrate: _local_env
	docker-compose -f docker-compose.yml run --rm web python manage.py migrate --noinput

migrations: _local_env
	docker-compose -f docker-compose.yml run --rm web python manage.py makemigrations

superuser: _local_env
	docker-compose -f docker-compose.yml run --rm web python manage.py createsuperuser

shell: _local_env
	docker-compose -f docker-compose.yml run --rm web python manage.py shell

service-port:
	docker-compose -f docker-compose-local.yml run --service-ports web

test: _local_env
	docker-compose -f docker-compose.yml run --rm web pytest
