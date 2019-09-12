from . import github_api
from flask import render_template


def generate_project_pages():
    repos = github_api.get_repositories()
    for repo in repos:
        generate_project_page(repo)


def generate_index():
    context = {'repos': github_api.get_repositories()}
    return render_template('index.html', **context)


def generate_project_page(repo: github_api.Repository):
    pass
