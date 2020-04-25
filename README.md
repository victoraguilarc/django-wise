## API StarterKit


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

#### Minimal Frontend
This projeect contains minimal frontend to some transactional fallback windows specially.
If you want to use it, run the following commands:

  * `npm install --global gulp-cli` Install gulp
  * `npm install` Install nodejs dependencies
  * `gulp` generate `css`, `js`  production files.
   
#### Pre commit actions
  * `make isort` Fix posible import issues
  * `make lint` Check code quality based on PEP-8 styleguidees
  * `make tests` Run the tests with unittest
  * `make pytest` Run the tests with pytest
