from . import github_api
from flask import render_template


def generate_project_pages():
    pass


def generate_index():
    context = {'repos': github_api.get_repos()}
    return render_template('index.html', **context)
