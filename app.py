from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = 'bananaboatxyz987'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False 
debug = DebugToolbarExtension(app)

RESPONSES_KEY ="responses"
# 370-263-852

@app.route('/')
def show_survey_info():
    """show home page for survey site"""

    title = survey.title
    instructions = survey.instructions
    return render_template('info.html', title = title, instructions= instructions)

@app.route('/start', methods=['POST'])
def start_survey():
    """Set session responses to empty list"""
    session[RESPONSES_KEY] = []

    return redirect('/questions/0')

@app.route('/questions/<int:index>')
def send_to_next_question(index):
    """shows user correct question form"""
    responses = session.get(RESPONSES_KEY)

    if responses is None:
        return redirect('/')
    if (len(responses) == len(survey.questions)):
        return redirect('/complete')
    if (len(responses) != index):
        flash(f'invalid question id: {index}.')
        return redirect(f'/questions/{len(responses)}')

    current_question= survey.questions[index]
    return render_template('form.html',question_num=index, question=current_question)

@app.route('/answer', methods=['POST'])
def handle_questions():
    """handle questions POST request"""
    answer = request.form['answer']
    
    responses = session[RESPONSES_KEY]
    responses.append(answer)
    session[RESPONSES_KEY]

    flash('answer submitted', 'success')

    if(len(responses) == len(survey.questions)):
        return redirect('/complete')

    return redirect(f'/questions/{len(responses)}')

@app.route("/complete")
def complete():
    """survey ended- show completion page"""

    return render_template('complete.html')

