run:
	FLASK_APP=portfolio_page FLASK_ENV=development flask run

run-public:
	FLASK_APP=portfolio_page FLASK_ENV=development flask run --host 0.0.0.0

tests:
	python -m pytest

.PHONY: tests
