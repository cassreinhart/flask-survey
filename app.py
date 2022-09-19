from flask import Flask, request, render_template, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = 'bananaboatxyz987'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False 
debug = DebugToolbarExtension(app)

responses = []
# 370-263-852

@app.route('/')
def show_survey_info():
    """show home page for survey site"""
    title = survey.title
    instructions = survey.instructions
    return render_template('info.html', title = title, instructions= instructions)

@app.route('/questions/<int:index>')
def send_to_next_question(index):
    """shows user correct question form"""

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
    
    responses.append(answer)
    flash('answer submitted', 'success')

    if(len(responses) == len(survey.questions)):
        return redirect('/complete')

    return redirect(f'/questions/{len(responses)}')

@app.route("/complete")
def complete():
    """survey ended- show completion page"""

    return render_template('complete.html')

