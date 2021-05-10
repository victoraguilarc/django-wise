.PHONY: docs coverage fixtures
.SILENT: clean
.PRECIOUS: lint

COMPOSE := docker-compose -f docker-compose.yml -f compose/docker-compose.dev.yml
COMPOSE_TEST := $(COMPOSE) -f compose/docker-compose.test.yml

ARG=

help:
	@echo
	@echo ----------------------------------------------------------------------
	@echo "   Development commands file                                        "
	@echo ----------------------------------------------------------------------
	@echo ">  R U N N I N G"
	@echo "  - build			            Build the containers for development"
	@echo "  - up			                Run & Up development server"
	@echo "  - superuser              Create a super user in the database"
	@echo "  - clean			            Stop & Destroy project containers"
	@echo "  - stop			              Stop compose runing"
	@echo "  - restart			          Restart compose running"
	@echo "  - clean_volumes          Destroy compose projet volumes"
	@echo "  - show_urls             	Show available routes"

	@echo ----------------------------------------------------------------------
	@echo ">  D E B U G I N G"
	@echo "  - debug			            Run & Up development server with ports for debuging"
	@echo "  - printenv			          Show all environmeent variables"
	@echo "  - settings			          Show computed django settings"
	@echo "  - console			          Open a Django shell console"
	@echo "  - dbshell			          Open a Database shell console"

	@echo ----------------------------------------------------------------------
	@echo ">  D A T A B A S E"
	@echo "  - fixtures			            Load testing data"
	@echo "  - dumpdata			            Generate testing data"
	@echo "  - migrate			            Apply unapplied migrations"
	@echo "  - migrations ARG={app}     Create deetected migrations automatically"
	@echo "  - squashmigrations			    Squash existent migrations"
	@echo "  - flushdb			            Drop database registries"

	@echo ----------------------------------------------------------------------
	@echo ">  T E S T I N G"
	@echo "  - tests			            Run tests"
	@echo "  - selenium			          Open selenium session to see them with VNC"
	@echo "  - pytest			            Run tests with pytest engine"
	@echo "  - clean_tests			      Running tests with pytest cleaning cache"
	@echo "  - coverage_tests			    Generate the coverage"
	@echo "  - coverage_report			  Generate coverage html report"
	@echo ----------------------------------------------------------------------
	@echo ">  L I N T I N G"
	@echo "  - lint			            Build the containers for development"

build:
	$(COMPOSE) build
	@echo "Building..."

up:
	@echo "Server up..."
	$(COMPOSE) up

run:
	$(COMPOSE) run --rm django $(ARG)


debug:
	@echo "Launchings Server for debbugging..."
	$(COMPOSE) run --service-ports django

loaddata:
	@echo "Loading fixtures..."
	$(COMPOSE) run --rm django python manage.py loaddata $(ARG)

fixtures:
	@echo "Loading fixtures..."
	$(COMPOSE) run --rm django python manage.py loaddata users

dumpdata:
	@echo "Getting fixtures..."
	$(COMPOSE) run --rm django python manage.py dumpdata $(ARG)

superuser:
	@echo "Creating superuser..."
	$(COMPOSE) run --rm django python manage.py createsuperuser

migrate:
	@echo "Applying migrations ..."
	$(COMPOSE) run --rm django python manage.py migrate $(ARG)

migrations:
	@echo "Creating migrations ..."
	$(COMPOSE) run --rm django python manage.py makemigrations $(ARG)

squashmigrations:
	@echo "Creating migrations ..."
	$(COMPOSE) run --rm django python manage.py squashmigrations $(APP)

settings:
	@echo "Opening django compiled settings ..."
	$(COMPOSE) run --rm django python manage.py diffsettings

flushdb:
	@echo "Flushing database ..."
	$(COMPOSE) run --rm django python manage.py flush

# Window version: docker ps -aq |  %{docker stop $_}
clean:
	@echo "Cleaning containers ..."
	docker ps -aq | xargs docker stop
	docker ps -aq | xargs docker rm

console:
	@echo "Opening django shell for testing and debbugging"
	$(COMPOSE) run --rm django python manage.py shell_plus

shell:
	@echo "Opening container bash session"
	$(COMPOSE) run --rm django bash

dbshell:
	@echo "Opening database shell"
	$(COMPOSE) run --rm django python manage.py dbshell

stop:
	@echo "Stopping containers"
	docker ps -qa | xargs docker stop

restart: stop up
	@echo "Containers restarted"

clean_volumes:
	@echo "Cleaning volumes ..."
	docker volume ls -q | grep django-wise | xargs docker volume rm
	docker images | grep "^<none>" | awk '{print $3}' | xargs docker rmi

show_urls:
	@echo "Show api routes"
	$(COMPOSE) run --rm django python manage.py show_urls


selenium:
	@echo "Starting selenium..."
	$(COMPOSE) start selenium

printenv:
	$(COMPOSE) run --rm django python merge_envs.py
	@echo "New [.env] file generated"

test:
	@echo "Running tests with pytest cleaning cache..."
	$(COMPOSE_TEST) run --rm django bash -c "DJANGO_ENV=testing pytest --pyargs $(ARG)"

clean_tests:
	$(COMPOSE_TEST) run --rm django pytest -n auto --pyargs --cache-clear

coverage:
	$(COMPOSE_TEST) run django coverage run -m pytest
	$(COMPOSE_TEST) run --rm django coverage report
	$(COMPOSE_TEST) run --rm django coverage html
	$(COMPOSE_TEST) run --rm django rm -f web/badges/coverage.svg
	$(COMPOSE_TEST) run --rm django coverage-badge -o web/badges/coverage.svg

coverage_tests:
	$(COMPOSE_TEST) run django coverage run -m pytest
	$(COMPOSE_TEST) run --rm django coverage html
	$(COMPOSE_TEST) run --rm django coverage json

lint:
	@echo "Verifying the code"
	$(COMPOSE) run --rm django flake8 $(ARG)

bash:
	@echo "Opening a shell session"
	$(COMPOSE) run --rm django sh

isort:
	@echo "Opening a shell session"
	$(COMPOSE) run --rm django isort .

locales:
	@echo "Generate traslations"
	$(COMPOSE) run --rm django python manage.py makemessages -l en
	$(COMPOSE) run --rm django python manage.py makemessages -l es

compile_locales:
	@echo "Compile traslations"
	$(COMPOSE) run --rm django python manage.py compilemessages

production_up:
	@echo "Server up..."
	docker-compose -f docker-compose.yml -f docker-compose.prod.yml up

report_coverage:
	@echo "Running coverage report"
	cd reports/coverage && python -m SimpleHTTPServer 3000

report_lint:
	@echo "Running coverage report"
	$(COMPOSE) run --rm django flake8 --format=html && cd reports/flake8 && python -m SimpleHTTPServer 3001

