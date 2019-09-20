import requests
import typing
from typing import List, Optional
from dataclasses import dataclass

from .helper import cache, report_error

GITHUB_USERNAME = "henne90gen"
repo_cache_path = "repositories.pickle"
readme_cache_path = "readme_{}.pickle"


@dataclass
class User:
    login: str
    id: int
    node_id: str
    avatar_url: str
    gravatar_id: str
    url: str
    html_url: str
    followers_url: str
    following_url: str
    gists_url: str
    starred_url: str
    subscriptions_url: str
    organizations_url: str
    repos_url: str
    events_url: str
    received_events_url: str
    type: str
    site_admin: bool


@dataclass
class Repository:
    id: int
    node_id: str
    name: str
    full_name: str
    private: bool
    owner: User
    html_url: str
    description: str
    fork: bool
    url: str
    forks_url: str
    keys_url: str
    collaborators_url: str
    teams_url: str
    hooks_url: str
    issue_events_url: str
    events_url: str
    assignees_url: str
    branches_url: str
    tags_url: str
    blobs_url: str
    git_tags_url: str
    git_refs_url: str
    trees_url: str
    statuses_url: str
    languages_url: str
    stargazers_url: str
    contributors_url: str
    subscribers_url: str
    subscription_url: str
    commits_url: str
    git_commits_url: str
    comments_url: str
    issue_comment_url: str
    contents_url: str
    compare_url: str
    merges_url: str
    archive_url: str
    downloads_url: str
    issues_url: str
    pulls_url: str
    milestones_url: str
    notifications_url: str
    labels_url: str
    releases_url: str
    deployments_url: str
    created_at: str
    updated_at: str
    pushed_at: str
    git_url: str
    ssh_url: str
    clone_url: str
    svn_url: str
    homepage: str
    size: int
    stargazers_count: int
    watchers_count: int
    language: str
    has_issues: bool
    has_projects: bool
    has_downloads: bool
    has_wiki: bool
    has_pages: bool
    forks_count: int
    mirror_url: str
    archived: bool
    disabled: bool
    open_issues_count: int
    license: str
    forks: int
    open_issues: int
    watchers: int
    default_branch: str
    network_count: int = 0
    subscribers_count: int = 0


def dict_to_user(d: dict) -> User:
    return User(**d)


def dict_to_repository(d: dict) -> Repository:
    if 'owner' in d:
        d['owner'] = dict_to_user(d['owner'])
    return Repository(**d)


@cache(repo_cache_path)
def get_repositories() -> List[Repository]:
    r = requests.get(f"https://api.github.com/users/{GITHUB_USERNAME}")
    if not r.ok:
        report_error(r)
        return None

    data = r.json()
    r = requests.get(data['repos_url'])
    if not r.ok:
        report_error(r)
        return None

    data = r.json()

    return list(map(dict_to_repository, data))


def get_repository(name: str) -> Repository:
    r = requests.get(f"https://api.github.com/repos/{GITHUB_USERNAME}/{name}")
    if not r.ok:
        report_error(r)
        return None

    data = r.json()
    return dict_to_repository(data)


def _get_readme_cache_path(repo: Repository):
    return readme_cache_path.format(repo.name)


@cache(_get_readme_cache_path)
def get_readme(repo: Repository) -> Optional[str]:
    r = requests.get(f"{repo.url}/readme")
    if not r.ok:
        report_error(r)
        return None

    data = r.json()
    r = requests.get(data['download_url'])
    return r.text


def get_resource_url(name: str, resource: str) -> str:
    return f"https://raw.githubusercontent.com/{GITHUB_USERNAME}/{name}/master/{resource}"
