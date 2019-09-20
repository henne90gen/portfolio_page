from typing import List

from flask import Flask

from portfolio_page import github_api
from portfolio_page.generator import create_landing_page, generate_project_pages


def test_generate_index(app: Flask, repos: List[github_api.Repository]):
    github_api.get_repositories = lambda: repos
    with app.app_context():
        result = create_landing_page()
        # print(result)
        # assert result is None
