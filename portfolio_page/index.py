from flask import Blueprint

bp = Blueprint('index', __name__)


@bp.route('/', methods=('GET',))
def root():
    return "Hello world"
