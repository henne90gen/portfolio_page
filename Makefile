run:
	FLASK_APP=portfolio_page FLASK_ENV=development flask run

tests:
	python -m pytest

.PHONY: tests
