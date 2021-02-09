import functools

from flask import Blueprint, redirect, render_template, request

bp = Blueprint('application', __name__, url_prefix='/')


@bp.route('/', methods=('GET',))
def index():
    return render_template('index/index.html.j2')
