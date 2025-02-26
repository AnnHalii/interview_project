IMAGE ?= interview_project:develop
COMPOSE ?= docker-compose

.EXPORT_ALL_VARIABLES:

.default: run

run:  build
	$(COMPOSE) up -d

stop:
	$(COMPOSE) stop

logs:
	$(COMPOSE) logs -f web

exec:
	$(COMPOSE) exec -it web bash

destroy:
	$(COMPOSE) down

test:
	$(COMPOSE) run --rm api-test

build:
	docker build -t $(IMAGE) .