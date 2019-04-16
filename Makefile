start:
	yarn compile
	pipenv run python run.py

compile:
	yarn compile

build:
	pipenv install --dev

lint:
	pipenv run flake8 ./app
	pipenv run pylint --output-format=colorized -j 0 --reports=n ./app

check:
	pipenv check

test: check lint
	pipenv run pytest tests --cov-report term-missing --cov app --capture no

stub_services:
	pipenv run python stubs/stub_services.py

smoke_test:
	pipenv run behave tests/functional/smoke_tests/features