# Maze generator site

Simple little maze maker + display site

## Install required modules

`$ pip install -r requirements.txt`

## Setup database

`$ export FLASK_APP=application.py`

`$ flask db init`

`$ flask db migrate`

`$ flask db upgrade`

## Check folder permissions

`application/static/maze_files` must be `read/write` if you wish to reset the database

## Run application

`$ flask run`