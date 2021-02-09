import functools

from flask import Blueprint, redirect, render_template, request

bp = Blueprint('application', __name__, url_prefix='/')


@bp.route('/', methods=('GET',))
def index():
    return render_template('application/index.html.j2')


@bp.route('/qna', methods=('GET', 'POST'))
def qna():
    if request.method == 'POST':
        pass
    return render_template('application/qna.html.j2')
