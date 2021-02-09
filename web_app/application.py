import functools

from flask import Blueprint, redirect, render_template, request, session
from flask.helpers import url_for

bp = Blueprint('application', __name__, url_prefix='/')


@bp.route('/', methods=('GET',))
def index():
    return render_template('application/index.html.j2')


@bp.route('/qna', methods=('GET', 'POST'))
def qna():
    if request.method == 'POST':
        context_para = request.form['context']
        questions = [
            request.form['question1'],
            request.form['question2'],
            request.form['question3'],
        ]
        session['context_para'] = context_para
        session['questions'] = questions
        return redirect(url_for('answers'))

    return render_template('application/qna.html.j2')
