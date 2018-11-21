.PHONY: test coverage isort check-isort check-flake8

test:
	tox

coverage:
	python-coverage erase
	-rm -r htmlcov
	tox
	python-coverage html -d htmlcov
