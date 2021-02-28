## Table of Contents
  - [What it does](#what-it-does)
  - [Virtual Environment Setup](#virtual-environment-setup)
  - [Database Setup](#database-setup)
  - [API Contract](#api-contract)
  - [Schema](#schema)
  - [Dependencies](#dependencies)
  - [Testing](#testing)
  - [Learning Goals](#learning-goals)
  - [Licenses](#licenses)
  - [Contact](#contact)
  - [Acknowledgments](#acknowledgments)

## What it does

This repository is part of a service-oriented architecture application that allows users to report indivdual experiences with unidentified flying objects and/or extraterrestrial beings. Serving as the backend to the ufomg-fe repository, ufomg_be takes user input and creates unique instances of encounter reports. In the spirit of the project's theme, there is no account registration or account login...users may remain annonymous. Users also have the ability to leave comments on individual sightings.

To view the production site, please visit the [UFOMG link](in_progress).

To view the other components of the application please visit the [Github Project Organization](https://github.com/UFOMG).

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
## API Contract

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
