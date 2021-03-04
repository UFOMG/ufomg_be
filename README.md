# README
<!-- Shields -->
![](https://img.shields.io/badge/Python-v3.9-blue)
![](https://img.shields.io/badge/Framework-Flask-yellow)
![](https://img.shields.io/badge/DB-PostgreSQL-blue)
![](https://img.shields.io/travis/com/UFOMG/ufomg_be)
![](https://img.shields.io/github/contributors/UFOMG/ufomg_be)
![](https://img.shields.io/badge/UFOMG-BE-green)
![](https://img.shields.io/github/issues/UFOMG/ufomg_be)
# UFOMG_BE

## Table of Contents
  - [What it does](#what-it-does)
  - [Contributors](#contributors)
  - [Schema](#schema)
  - [Virtual Environment Setup](#virtual-environment-setup)
  - [Database Setup](#database-setup)
  - [API Endpoints](#api-endpoints)
  - [Dependencies](#dependencies)
  - [Testing](#testing)
  - [Learning Goals](#learning-goals)
  - [Licenses](#licenses)
  - [Acknowledgments](#acknowledgments)

## What it does

This repository is part of a service-oriented architecture application that allows users to report indivdual experiences with unidentified flying objects and/or extraterrestrial beings. Serving as the backend to the ufomg-fe repository, ufomg_be takes user input and creates unique instances of encounter reports. In the spirit of the project's theme, there is no account registration or account login...users may remain annonymous. Users also have the ability to leave comments on individual sightings.

To view the front-end production site, please visit the [UFOMG link](http://ufomfg.herokuapp.com/).

To view the other components of the application please visit the [Github Project Organization](https://github.com/UFOMG).

## Contributors

- Austin Aspaas  [Github](https://gist.github.com/evilaspaas1) | [LinkedIn](https://www.linkedin.com/in/austin-aspaas-4626611bb/)
- Hanna Davis  [Github](https://github.com/Oxalisviolacea) | [LinkedIn](https://www.linkedin.com/in/hanna-davis/)
- Philip DeFraties  [Github](https://github.com/philipdefraties) | [LinkedIn](https://www.linkedin.com/in/philip-defraties/)
- Todd Estes  [Github](https://github.com/Todd-Estes) | [LinkedIn](https://www.linkedin.com/in/toddwestes/)

## Schema
<img src="https://github.com/UFOMG/ufomg_be/blob/main/schema_diagram.png" width="800" height="400" />
  
## Virtual Environment Setup

For usage on your local machine follow the instructions listed below:

```
git clone git@github.com:UFOMG/ufomg_be.git
cd ufomg_be

# build a virtual environment to install your Python packages
python3 -m venv ./venv

# 'activate' the virtual environment for your project
# do this every time you start a new terminal and enter your project folder
source venv/bin/activate

# install your Python packages
pip3 install -r requirements.txt

To shut off your virtual environment, run deactivate at a terminal where you have an active virtual environment.
```

## Database Setup

```
createdb ufomg_dev
createdb ufomg_test

export DATABASE_URL=postgresql://localhost:5432/ufomg_dev

# examine any database models you have set up
python3 manage.py db migrate

# "upgrade" your database schema to use the changes you've made in your models
python3 manage.py db upgrade

# then apply the same for your test database:
export DATABASE_URL=postgresql://localhost:5432/ufomg_test
python3 manage.py db upgrade

```
## API Endpoints

To see an example response like that below you can use [Postman](https://www.postman.com/) to send a GET request to our BE hosted on Heroku here: https://ancient-mesa-60922.herokuapp.com/api/v1/reports

![Screen Shot 2021-03-01 at 2 28 33 PM](https://user-images.githubusercontent.com/66448493/109561749-d7435b00-7a9a-11eb-8dc7-418175c5b755.png)


Required parameters:

GET /api/v1/users
Description:

fetches all users in the database
returns 200 status code on success
Required Request Headers:

none
Required Request Body:

none
Response Body: (TBD)


## Dependencies
```
Flask==1.1.2
Flask-RESTful==0.3.8
Flask-SQLAlchemy==2.4.4
psycopg2-binary==2.8.6
SQLAlchemy==1.3.19
flask_migrate==2.5.3
flask-script==2.0.6
Flask-Cors==3.0.9
bleach==3.2.1
pytest==6.1.0
coverage==5.3
gunicorn==20.0.4
pep8==1.7.1
pycodestyle==2.6.0
```  
  
## Testing
```
export DATABASE_URL=postgresql://localhost:5432/ufomg_test
pytest
```
There should be 44 passing tests with 100% test coverage.
