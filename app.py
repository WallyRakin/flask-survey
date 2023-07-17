from surveys import satisfaction_survey
from flask import Flask, request, session, flash, redirect, render_template


app = Flask(__name__)
app.secret_key = 'your_secret_key_here'


@app.route("/")
def survey():
    session['responses'] = []
    print(session['responses'])
    return render_template('survey.html', survey=satisfaction_survey)


@app.route("/questions/<num>")
def question(num):
    responses = session['responses']
    print(num, responses)
    if len(responses) == len(satisfaction_survey.questions):
        return redirect('/thanks')
    if not (int(num) == len(responses)):
        flash('Questions must be answered in order')
        return redirect(f'/questions/{len(responses)}')
    return render_template('question.html', question=satisfaction_survey.questions[int(num)], next=int(num)+1, last=len(satisfaction_survey.questions))


@app.route("/thanks")
def thanks():
    return render_template('thanks.html')


@app.route("/answer", methods=["POST"])
def answer():
    responses = session['responses']
    answer = request.form.get("answer")
    next = request.form.get("next")
    if answer == None:
        flash('Must fill in an answer')
        return redirect(f'/questions/{int(next)-1}')
    last = request.form.get("last")
    responses.append(answer)
    session['responses'] = responses
    if not (int(next) == len(session['responses'])):
        return f'fail: {answer}, {next}, {responses}'
    if next <= last:
        print(next, last, len(session['responses']), len(
            satisfaction_survey.questions))
        return redirect(f'/questions/{next}')
    else:
        return redirect('/thanks')


app.run(debug=True)
