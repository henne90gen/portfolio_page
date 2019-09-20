import os
from typing import List, Optional
from dataclasses import dataclass
from flask import render_template, render_template_string, Markup

from . import github_api
from .helper import cache
from .markdown_renderer import render_markdown


@dataclass
class Project:
    title: str
    url: str
    short_description: Markup = Markup("")


def create_project(repo: github_api.Repository) -> Project:
    readme = github_api.get_readme(repo)
    project = Project(repo.name, repo.name)
    if readme is None:
        project.short_description = Markup("No README available")
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

    project.short_description = render_markdown(result, repo.name)
    return project


def remove_forks(repo: github_api.Repository) -> bool:
    return not repo.fork


def create_landing_page():
    repos = github_api.get_repositories()
    if repos is None:
        return render_template('error.html')

    repos = list(filter(remove_forks, repos))
    projects = list(map(create_project, repos))
    context = {'projects': projects}
    return render_template('index.html', **context)


def generate_project_pages():
    repos = github_api.get_repositories()
    for repo in repos:
        generate_project_page(repo)


def generate_project_page(repo: github_api.Repository):
    readme = github_api.get_readme(repo)
    if readme is None:
        return "No README available"

    project = create_project(repo)
    readme_rendered = render_markdown(readme.split("\n"), repo.name)
    context = {'readme': readme_rendered, 'project': project}
    return render_template("project.html", **context)


def _get_project_cache_name(name: str):
    return f"{name}.html"


def create_project_page(name: str) -> str:
    repo = github_api.get_repository(name)
    return generate_project_page(repo)
