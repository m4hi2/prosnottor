import functools

import torch
from flask import Blueprint, redirect, render_template, request, session
from flask.helpers import url_for
from transformers import AutoTokenizer, BertForQuestionAnswering

modelpath = "./forqa"
tokenizer = AutoTokenizer.from_pretrained(modelpath)
model = BertForQuestionAnswering.from_pretrained(modelpath)

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
        return redirect(url_for('application.answers'))

    return render_template('application/qna.html.j2')


@bp.route('/answers', methods=('GET',))
def answers():
    context_para = session.get('context_para')
    questions = session.get('questions')
    _qna = dict()

    for question in questions:
        tokens = tokenizer(question, context_para,
                           add_special_tokens=True, return_tensors="pt")
        input_ids = tokens["input_ids"].tolist()[0]
        text_tokens = tokenizer.convert_ids_to_tokens(input_ids)
        # print(inputs)
        outputs = model(**tokens)
        start_scores = outputs.start_logits
        end_scores = outputs.end_logits

        # print(start_scores, end_scores)

        start_index = torch.argmax(start_scores)

        end_index = torch.argmax(end_scores)

        answer = ' '.join(text_tokens[start_index:end_index+1])
        corrected_answer = ''

        for word in answer.split():

            # If it's a subword token
            if word[0:2] == '##':
                corrected_answer += word[2:]
            else:
                corrected_answer += ' ' + word
        _qna[question] = corrected_answer

    return render_template(
        'application/answers.html.j2',
        qnas=_qna,
        para=context_para
    )
