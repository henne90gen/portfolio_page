import os
import requests
import typing
from typing import List, Optional, Union, Callable, Any
from dataclasses import dataclass
import pickle

GITHUB_USERNAME = "henne90gen"
cache_directory = "cache"
repo_cache_path = "cache/repositories.pickle"
readme_cache_path = "cache/readme_{}.pickle"


def cache(path_or_path_func: Union[str, Callable[[Any], str]]):
    """
    This decorator caches the result of a function in a file.
    The decorated function is only executed the very first time.
    Any further calls will return the cached result.
    """
    def wrapper(func):
        def inner(*args, **kwargs):
            if not os.path.exists(cache_directory):
                os.mkdir(cache_directory)

            path = path_or_path_func
            if callable(path_or_path_func):
                path = path_or_path_func(*args, **kwargs)

            if not os.path.exists(path):
                result = func(*args, **kwargs)
                with open(path, 'wb+') as f:
                    pickle.dump(result, f)
            else:
                with open(path, 'rb') as f:
                    result = pickle.load(f)

            return result
        return inner
    return wrapper


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


def dict_to_user(d: dict) -> User:
    return User(**d)


def dict_to_repository(d: dict) -> Repository:
    d['owner'] = dict_to_user(d['owner'])
    return Repository(**d)


@cache(repo_cache_path)
def get_repositories() -> List[Repository]:
    r = requests.get(f"https://api.github.com/users/{GITHUB_USERNAME}")
    data = r.json()
    r = requests.get(data['repos_url'])
    data = r.json()

    return list(map(dict_to_repository, data))


def _get_readme_cache_path(repo: Repository):
    return readme_cache_path.format(repo.name)


@cache(_get_readme_cache_path)
def get_readme(repo: Repository) -> Optional[str]:
    r = requests.get(f"{repo.url}/readme")
    if not r.ok:
        return None

    data = r.json()
    r = requests.get(data['download_url'])
    return r.text
