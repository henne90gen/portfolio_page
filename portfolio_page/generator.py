from typing import List, Optional
from dataclasses import dataclass
from flask import render_template, render_template_string, Markup

from . import github_api


@dataclass
class Project:
    title: str
    short_description: Markup = Markup("")


def render_images(line):
    result = ""
    while "![" in line:
        start_index = line.find("![")
        before = line[:start_index]
        line = line[start_index + 2:]

        name_end = line.find(']')
        title = line[:name_end]
        line = line[name_end + 2:]

        url_end = line.find(")")
        url = line[:url_end]
        line = line[url_end + 1:]

        image = render_template_string(
            "<img src=\"{{ url }}\" title=\"{{ title }}\"/>", url=url, title=title)
        result += before + image

    result += line
    return result


def render_links(line):
    result = ""
    while "[" in line:
        start_index = line.find("[")
        before = line[:start_index]
        line = line[start_index + 1:]

        content_end = line.find('](')
        content = Markup(line[:content_end])
        line = line[content_end + 2:]

        url_end = line.find(')')
        url = line[:url_end]
        line = line[url_end + 1:]

        link = render_template_string(
            "<a href=\"{{ url }}\">{{ content }}</a>", url=url, content=content)
        result += before + link
    result += line
    return result


def render_tables(lines: List[str]):
    return lines


def render_markdown(lines: str) -> Markup:
    result = list(map(render_links, map(render_images, lines)))
    result = render_tables(result)
    return Markup("<br>".join(result))


def create_project(repo: github_api.Repository) -> Project:
    readme = github_api.get_readme(repo)
    project = Project(repo.name)
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

    project.short_description = render_markdown(result)
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
