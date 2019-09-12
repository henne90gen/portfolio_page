from flask import Blueprint, render_template

from .generator import create_landing_page

bp = Blueprint('index', __name__)


@bp.route('/', methods=('GET',))
def root():
    return create_landing_page()
