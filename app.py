from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

responses = []

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'

debug = DebugToolbarExtension(app)

@app.route('/')
def start_page():
    return render_template('start_page.html', survey = survey)

@app.route('/start', methods = ['POST'])
def start_survey():
    session[responses] = []
    return redirect('/questions/0')

@app.route('/answer', methods = ['POST'])
def answer_question():
    answer = request.form['answer']

    responses = session[responses]
    responses.append(answer)
    session[responses] = responses

    if(len(responses) == len(survey.questions)):
        return redirect('/finished')
    else: 
        return redirect(f'/questions/{len(responses)}')
    
@app.route('/finished')
def finished():
    return render_template('thank_you_page.html')

@app.route('/questions/<int:id>')
def question(id):
    if(len(responses) != id):
        flash(f'Trying to access invalid question: {id}.')
        return redirect(f'/questions/{len(responses)}')
    
    if(len(responses) == len(survey.questions)):
        return redirect('/finished')

    if not responses:
        return redirect('/')
    
    question = survey.questions[id]
    return render_template('question.html', question_id = id, question = question)

