from flask import Blueprint, render_template, redirect, send_from_directory

from .generator import create_landing_page, create_project_page
from .github_api import get_resource_url

bp = Blueprint('index', __name__, static_url_path='static')


@bp.route('/', methods=('GET',))
def root():
    return create_landing_page()


@bp.route('/favicon.ico')
def favicon():
    return redirect('/static/favicon.svg')


@bp.route('/<string:name>', methods=('GET',))
def project_page(name: str):
    return create_project_page(name)


@bp.route('/<string:name>/<path:resource>', methods=('GET',))
def project_page_resources(name: str, resource: str):
    return redirect(get_resource_url(name, resource))
