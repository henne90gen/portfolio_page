import pytest

from flask import Flask
from flask.testing import FlaskClient

from portfolio_page import create_app, github_api
from portfolio_page.generator import generate_index, generate_project_pages


@pytest.fixture
def app():
    return create_app({'TESTING': True})


@pytest.fixture
def client(app: Flask):
    return app.test_client()


def test_generate_index(app: Flask):
    repos = {}
    github_api.get_repos = lambda: repos
    with app.app_context():
        result = generate_index()
        print(result)
        assert result is None
