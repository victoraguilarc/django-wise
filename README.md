## Wise API Boilerplate

This is an opinionated boilerplate to start django projects

![styleguide](https://img.shields.io/badge/styleguide-flake8-blue)
![Coverage](web/badges/coverage.svg) 

### Stack

  * [Django](https://www.djangoproject.com/) as main web Framework
  * [Django Rest Framework](http://www.django-rest-framework.org/) as API development tooling
  * [Postgres](http://www.django-rest-framework.org/) for SQL Database
  * [Django Q](http://www.django-rest-framework.org/) for scheduled and async tasks.
  * [Docker/docke-compose](http://www.django-rest-framework.org/) for development and standalone deployments.


### Features
  - [x] Registration
  - [x] Autthentication (JWT Token, OTP)
  - [x] Accounts (Users/Devices)
  - [x] Social Networks Support (Facebook/Google).
  - [ ] API Documentation

## Getting started

You need to have installed `git`, `docker`, `ssh` and a decent `terminal`.

  1. `make build` build the images for development. 
  2. `make fixtures` load initial data (optional). 
  3. `make up` start development server.

Probably you need to user the following command for another situations. 

  * `make django` to enable `debug` mode during development.
  * `make migrations` run django makemigrations command
  * `make migrate` run django migrate command
  * `make superuser` make a superuserfor develoment

### Testing

* `make test` run pytest over all test files in the project
* `make test ARG=path_to_file` run pytest of a single test file.
  
### Code Quality
* `make coverage` run pytest and generate the coverage report.
* `make lint` run flake8 and generate linting report.
* `make report_coverage` serves the coverage report as html at `localhost:3000`
* `make report_lint` serves the lint report as html at `localhost:3001`

### Pre commit actions
  * `make isort` Fix posible import issues
  * `make lint` Check code quality based on PEP-8 styleguidees
  * `make tests` Run the tests with unittest
  * `make pytest` Run the tests with pytest


## Transactional Frontend
This project has a transactional minimum frontend views, it is to process
flows like: 

 - Confirm Email
 - Reset password

The usage of these views are completely optional. If you want to testi it 
by yourself you need to have `nodejs` installed, after that run the 
following commands:
  * `npm install --global gulp-cli` Install gulp globally
  * `npm install` Install nodejs dependencies
  * `gulp` generate `css`, `js`  frontend assets.
