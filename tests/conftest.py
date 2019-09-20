import pytest

from flask import Flask
from flask.testing import FlaskClient
from portfolio_page import create_app, github_api

DEFAULT_REPOSITORY = {
    'id': 159038349,
    'node_id': 'MDEwOlJlcG9zaXRvcnkxNTkwMzgzNDk=',
    'name': 'structure_from_motion',
    'full_name':
    'henne90gen/structure_from_motion',
    'private': False,
    'owner': {'login': 'henne90gen', 'id': 1887241, 'node_id': 'MDQ6VXNlcjE4ODcyNDE=', 'avatar_url': 'https://avatars1.githubusercontent.com/u/1887241?v=4', 'gravatar_id': '', 'url': 'https://api.github.com/users/henne90gen', 'html_url': 'https://github.com/henne90gen', 'followers_url': 'https://api.github.com/users/henne90gen/followers', 'following_url': 'https://api.github.com/users/henne90gen/following{/other_user}', 'gists_url': 'https://api.github.com/users/henne90gen/gists{/gist_id}', 'starred_url': 'https://api.github.com/users/henne90gen/starred{/owner}{/repo}', 'subscriptions_url': 'https://api.github.com/users/henne90gen/subscriptions', 'organizations_url': 'https://api.github.com/users/henne90gen/orgs', 'repos_url': 'https://api.github.com/users/henne90gen/repos', 'events_url': 'https://api.github.com/users/henne90gen/events{/privacy}', 'received_events_url': 'https://api.github.com/users/henne90gen/received_events', 'type': 'User', 'site_admin': False},
    'html_url': 'https://github.com/henne90gen/structure_from_motion',
    'description': None,
    'fork': False,
    'url': 'https://api.github.com/repos/henne90gen/structure_from_motion',
    'forks_url': 'https://api.github.com/repos/henne90gen/structure_from_motion/forks',
    'keys_url': 'https://api.github.com/repos/henne90gen/structure_from_motion/keys{/key_id}',
    'collaborators_url': 'https://api.github.com/repos/henne90gen/structure_from_motion/collaborators{/collaborator}',
    'teams_url': 'https://api.github.com/repos/henne90gen/structure_from_motion/teams',
    'hooks_url': 'https://api.github.com/repos/henne90gen/structure_from_motion/hooks',
    'issue_events_url': 'https://api.github.com/repos/henne90gen/structure_from_motion/issues/events{/number}',
    'events_url': 'https://api.github.com/repos/henne90gen/structure_from_motion/events',
    'assignees_url': 'https://api.github.com/repos/henne90gen/structure_from_motion/assignees{/user}',
    'branches_url': 'https://api.github.com/repos/henne90gen/structure_from_motion/branches{/branch}',
    'tags_url': 'https://api.github.com/repos/henne90gen/structure_from_motion/tags',
    'blobs_url': 'https://api.github.com/repos/henne90gen/structure_from_motion/git/blobs{/sha}',
    'git_tags_url': 'https://api.github.com/repos/henne90gen/structure_from_motion/git/tags{/sha}',
    'git_refs_url': 'https://api.github.com/repos/henne90gen/structure_from_motion/git/refs{/sha}',
    'trees_url': 'https://api.github.com/repos/henne90gen/structure_from_motion/git/trees{/sha}',
    'statuses_url': 'https://api.github.com/repos/henne90gen/structure_from_motion/statuses/{sha}',
    'languages_url': 'https://api.github.com/repos/henne90gen/structure_from_motion/languages',
    'stargazers_url': 'https://api.github.com/repos/henne90gen/structure_from_motion/stargazers',
    'contributors_url': 'https://api.github.com/repos/henne90gen/structure_from_motion/contributors',
    'subscribers_url': 'https://api.github.com/repos/henne90gen/structure_from_motion/subscribers',
    'subscription_url': 'https://api.github.com/repos/henne90gen/structure_from_motion/subscription',
    'commits_url': 'https://api.github.com/repos/henne90gen/structure_from_motion/commits{/sha}',
    'git_commits_url': 'https://api.github.com/repos/henne90gen/structure_from_motion/git/commits{/sha}',
    'comments_url': 'https://api.github.com/repos/henne90gen/structure_from_motion/comments{/number}',
    'issue_comment_url': 'https://api.github.com/repos/henne90gen/structure_from_motion/issues/comments{/number}',
    'contents_url': 'https://api.github.com/repos/henne90gen/structure_from_motion/contents/{+path}',
    'compare_url': 'https://api.github.com/repos/henne90gen/structure_from_motion/compare/{base}...{head}',
    'merges_url': 'https://api.github.com/repos/henne90gen/structure_from_motion/merges',
    'archive_url': 'https://api.github.com/repos/henne90gen/structure_from_motion/{archive_format}{/ref}',
    'downloads_url': 'https://api.github.com/repos/henne90gen/structure_from_motion/downloads',
    'issues_url': 'https://api.github.com/repos/henne90gen/structure_from_motion/issues{/number}',
    'pulls_url': 'https://api.github.com/repos/henne90gen/structure_from_motion/pulls{/number}',
    'milestones_url': 'https://api.github.com/repos/henne90gen/structure_from_motion/milestones{/number}',
    'notifications_url': 'https://api.github.com/repos/henne90gen/structure_from_motion/notifications{?since,all,participating}',
    'labels_url': 'https://api.github.com/repos/henne90gen/structure_from_motion/labels{/name}',
    'releases_url': 'https://api.github.com/repos/henne90gen/structure_from_motion/releases{/id}',
    'deployments_url': 'https://api.github.com/repos/henne90gen/structure_from_motion/deployments',
    'created_at': '2018-11-25T14:08:43Z',
    'updated_at': '2019-02-10T19:02:24Z',
    'pushed_at': '2019-02-10T19:02:22Z',
    'git_url': 'git://github.com/henne90gen/structure_from_motion.git',
    'ssh_url': 'git@github.com:henne90gen/structure_from_motion.git',
    'clone_url': 'https://github.com/henne90gen/structure_from_motion.git',
    'svn_url': 'https://github.com/henne90gen/structure_from_motion',
    'homepage': None,
    'size': 13,
    'stargazers_count': 0,
    'watchers_count': 0,
    'language': 'Python',
    'has_issues': True,
    'has_projects': True,
    'has_downloads': True,
    'has_wiki': True,
    'has_pages': False,
    'forks_count': 0,
    'mirror_url': None,
    'archived': False,
    'disabled': False,
    'open_issues_count': 0,
    'license': None,
    'forks': 0,
    'open_issues': 0,
    'watchers': 0,
    'default_branch': 'master'
}


@pytest.fixture
def app():
    return create_app({'TESTING': True})


@pytest.fixture
def client(app: Flask):
    return app.test_client()


def create_repo(name: str):
    repo = github_api.Repository(**DEFAULT_REPOSITORY)
    repo.name = name
    return repo


@pytest.fixture
def repos():
    repos = [create_repo("test")]
    return repos
