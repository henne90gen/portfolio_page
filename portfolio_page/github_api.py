import requests


def get_repos():
    r = requests.get('https://api.github.com/users/henne90gen')
    data = r.json()
    r = requests.get(data['repos_url'])
    return r.json()
