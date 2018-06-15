from django.shortcuts import render
import requests


def index(request):
    """
    Homepage
    """
    r = requests.get('https://api.github.com/users/henne90gen')
    data = r.json()
    for key in data:
        print(key, data[key])
    r = requests.get(data['repos_url'])
    repos = r.json()
    for repo in repos:
        print(repo)
    return render(request, 'index.html')
