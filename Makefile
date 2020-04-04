#!/usr/bin/make -f

all: run

clean:
	rm -rf venv *.egg-info dist

venv: requirements-dev.txt requirements.txt
	python3 -m venv venv &&\
	venv/bin/pip install -r $< -e .

run: venv
	FLASK_APP=whatdo \
	FLASK_RUN_PORT=5000 \
	WHATDO_SETTINGS=../settings.cfg \
	venv/bin/flask run

test: venv
	WHATDO_SETTINGS=../settings.cfg \
	venv/bin/python -m unittest discover -s tests

lint: venv
	venv/bin/flake8 whatdo || r=1;\
	venv/bin/pylint whatdo || r=1;\
	exit $$r

check: lint test

sdist: venv test
	venv/bin/python setup.py sdist
