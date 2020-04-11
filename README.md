## DRF API StarterKit


![styleguide](https://img.shields.io/badge/styleguide-flake8-blue)
![Coverage](web/badges/coverage.svg) 


#### Features

  - [x] Registration
  - [x] Autthentication
  - [x] Social Networks Support (Facebook/Google).
   

## Development

#### Technologies

  * [Django](https://www.djangoproject.com/)
  * [Django Rest Framework](http://www.django-rest-framework.org/)

You need to have installed `git`, `docker`, `ssh` and and a good `terminal`.

#### Basic commands
  * `make build` build the images for development. 
  * `make server` run dev server.
  * `make django` enable deebugging server `debug`.
  * `make migrations` run django makemigrations command
  * `make migrate` run django migrate command
  * `make superuser` make a superuserfor develoment

#### Frontend
  * `npm install` Install nodejs dependencies
  * `gulp bundle` generate `css`, `js`  files for development.
  * `gulp bundle --prod` build `css`, `js` files for production
  * `gulp watch` start watch over static files for development
   
#### Pre commit actions
  * `make isort` Fix posible import issues
  * `make lint` Check code quality based on PEP-8 styleguidees
  * `make tests` Run the tests with unittest
  * `make pytest` Run the tests with pytest
