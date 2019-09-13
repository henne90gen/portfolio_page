from typing import List, Optional
from dataclasses import dataclass
from flask import render_template

from . import github_api

@dataclass
class Project:
    title: str
    short_description: str = ""


def create_project(repo: github_api.Repository) -> Project:
    readme = github_api.get_readme(repo)
    project = Project(repo.name)
    if readme is None:
        project.short_description = "No README available"
        return project

    lines = readme.split("\n")
    result = []
    for line in lines:
        if line.startswith('##'):
            break
        if line.startswith('# '):
            project.title = line[2:]
            continue
        result.append(line)

    project.short_description = "\n".join(result)    
    return project


def remove_forks(repo: github_api.Repository) -> bool:
    return not repo.fork


def create_landing_page():
    repos = list(filter(remove_forks, github_api.get_repositories()))

    projects = list(map(create_project, repos))
    context = {'projects': projects}
    return render_template('index.html', **context)


def generate_project_pages():
    repos = github_api.get_repositories()
    for repo in repos:
        generate_project_page(repo)


def generate_project_page(repo: github_api.Repository):
    pass
