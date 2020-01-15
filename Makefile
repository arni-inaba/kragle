.PHONY: test

setup:
	poetry install

test:
	poetry run pytest -vsx test/

test_%:
	poetry run pytest -vs -k $@ --pdb

lint:
	poetry run flake8 debouncer test
	poetry run mypy debouncer
