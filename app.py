from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

responses = []


@app.get("/")
def show_survey_home():
    """Show survey title, instructions, and a button"""

    return render_template("survey_start.html", survey=survey)


@app.post("/begin")
def start_survey():
    """Start the survey"""

    return redirect("/questions/0")

@app.get("/questions/<int:question_id>")
def show_question(question_id):
    """Show current question as form"""

    current_question = survey.questions[question_id]

    return render_template("question.html", question = current_question)
