import os
from typing import List, Optional
from dataclasses import dataclass
from flask import render_template, Markup

from . import github_api
from .markdown_renderer import render_short_description


@dataclass
class Project:
    title: str
    url: str
    short_description: Markup = Markup("")


def create_project(repo: github_api.Repository) -> Project:
    readme = github_api.get_readme(repo)
    project = Project(repo.name, repo.name)
    if readme is None:
        project.short_description = Markup("<div class=\"card-content\">No README available</div>")
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

    project.short_description = render_short_description(result, repo.name)
    return project


def remove_forks(repo: github_api.Repository) -> bool:
    return not repo.fork


def create_landing_page():
    repos = github_api.get_repositories()
    if repos is None:
        return render_template('error.html')

    repos = list(filter(remove_forks, repos))
    projects = list(sorted(map(create_project, repos), key=lambda p: p.url))
    context = {'projects': projects}
    return render_template('index.html', **context)


def generate_project_pages():
    repos = github_api.get_repositories()
    for repo in repos:
        generate_project_page(repo)


def correct_relative_links(html: str, path_prefix: str) -> str:
    if not path_prefix.endswith("/"):
        path_prefix += "/"

    def correct(text: str, url_attribute: str) -> str:
        url_attribute = url_attribute + "=\""
        attribute_size = len(url_attribute)
        index = text.find(url_attribute)
        while index != -1:
            is_internal_page_link = text[index + attribute_size] == "#"
            is_absolute_link = text[index + attribute_size:index + attribute_size + 4] == "http"
            if not is_absolute_link and not is_internal_page_link:
                first_part = text[:index + attribute_size]
                last_part = text[index + attribute_size:]
                text = first_part + path_prefix + last_part

            if is_internal_page_link:
                first_part = text[:index + attribute_size]
                last_part = text[index + attribute_size + 1:]
                text = first_part + "#user-content-" + last_part

            index = text.find(url_attribute, index + attribute_size)
        return text

    html = correct(html, "src")
    html = correct(html, "href")
    return html


def generate_project_page(repo: github_api.Repository):
    readme = github_api.get_readme_html(repo)
    if readme is None:
        return "No README available"

    readme = correct_relative_links(readme, repo.name)
    project = create_project(repo)
    context = {'readme': Markup(readme), 'project': project}
    return render_template("project.html", **context)


def _get_project_cache_name(name: str):
    return f"{name}.html"


def create_project_page(name: str) -> str:
    repo = github_api.get_repository(name)
    return generate_project_page(repo)
