.PHONY: clean-pyc init help test-ci
.DEFAULT_GOAL := help

help: ## See what commands are available.
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36mmake %-15s\033[0m # %s\n", $$1, $$2}'

init: clean-pyc ## Install dependencies and initialise for development.
	pip install --upgrade pip setuptools twine wheel
	pip install -r requirements.txt
	python manage.py migrate
	python manage.py loaddata fixtures/demo_data.json

lint: ## Lint the project.
	black --check **/*.py
	flake8 **/*.py
#	mypy **/*.py

format: ## Format project files.
	black **/*.py
	npm run format

test: ## Test the project.
	PYTHONDEVMODE=1 pytest --strict-config

test-watch: ## Restarts the tests whenever a file changes.
	PYTHONDEVMODE=1 nodemon -q -e py,json -w kontrasto  -x "clear && pytest --strict-config --exitfirst --new-first -q || true"

test-coverage: ## Run the tests while generating test coverage data.
	PYTHONDEVMODE=1 coverage run -m pytest --strict-config && coverage report

clean-pyc: ## Remove Python file artifacts.
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +

make dump-demo: ## One-off fixtures dump command to bootstrap demo sites from.
	python manage.py dumpdata --natural-foreign --natural-primary -e contenttypes -e auth.Permission -e sessions -e home.rendition -e wagtailcore.pagelogentry --indent 2 > fixtures/demo_data.json

make build-demo: ## Builds the demo site for static hosting.
	npm run build
	python manage.py collectstatic --no-input
	python manage.py migrate --no-input
	python manage.py flush --no-input
	python manage.py loaddata fixtures/demo_data.json
	DJANGO_VITE_DEV_MODE=false python manage.py runserver &
	wget --mirror --page-requisites http://localhost:8000/

sdist: ## Builds package version
	rm dist/* ; python setup.py sdist bdist_wheel

publish: sdist ## Publishes a new version to pypi.
	twine upload dist/*

publish-test: sdist ## Publishes a new version to test pypi.
	twine upload --repository-url https://test.pypi.org/legacy/ dist/*
