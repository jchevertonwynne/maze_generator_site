# Maze generator site

Simple little maze maker + display site

## Install required modules

`$ pip install -r requirements.txt`

## Setup database

`$ export FLASK_APP=application.py`

`$ flask db init`

`$ flask db migrate`

`$ flask db upgrade`

## Run application

`$ flask run`

### Open to internet

`$ sudo python3 flask run --host=0.0.0.0 --port=80`
