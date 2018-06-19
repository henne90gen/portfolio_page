from django.shortcuts import render
import requests


def fetch_repos():
    r = requests.get('https://api.github.com/users/henne90gen')
    data = r.json()
    r = requests.get(data['repos_url'])
    return r.json()


def fetch_project(project_name: str):
    r = requests.get(f'https://api.github.com/repos/henne90gen/{project_name}')
    data = r.json()
    return data


def index(request):
    """
    Homepage
    """
    context = {'repos': fetch_repos()}
    return render(request, 'index.html', context=context)


def project(request, name: str):
    context = {
        'repos': fetch_repos(),
        'project': fetch_project(name)
    }
    return render(request, 'project.html', context=context)
