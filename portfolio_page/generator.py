from typing import List, Optional
from dataclasses import dataclass
from flask import render_template

from . import github_api


def get_first_paragraph(readme: Optional[str]):
    if readme is None:
        return "No README available"

    lines = readme.split("\n")
    result = []
    for line in lines:
        if line.startswith('##'):
            break
        if line.startswith('#'):
            continue
        result.append(line)
    return "\n".join(result)


def remove_forks(repo: github_api.Repository) -> bool:
    return not repo.fork


def create_landing_page():
    repos = list(filter(remove_forks, github_api.get_repositories()))

    short_descriptions = {}
    for repo in repos:
        readme = github_api.get_readme(repo)
        short_descriptions[repo.name] = get_first_paragraph(readme)

    context = {'repos': repos, 'short_descriptions': short_descriptions}
    return render_template('index.html', **context)


def generate_project_pages():
    repos = github_api.get_repositories()
    for repo in repos:
        generate_project_page(repo)


def generate_project_page(repo: github_api.Repository):
    pass
