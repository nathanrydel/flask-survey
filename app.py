from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import surveys

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

SESSION_RESPONSES_KEY = "responses"


@app.get("/")
def show_survey_select_menu():
    """Show survey select menu for user to choose survey"""

    return render_template("survey_select.html", surveys=surveys)


@app.post("/selection")
def show_survey_home():
    """Show survey title, instructions, and a button. Clears
    session["responses"] on page load"""

    session[SESSION_RESPONSES_KEY] = []

    survey_title = request.form["survey_selection"]
    survey = surveys[survey_title]

    return render_template("survey_start.html",
                           survey=survey,
                           survey_key=survey_title)

# TODO: Add survey variables to all non-root endpoints for tracking


@app.post("/begin")
def start_survey():
    """Start the survey"""

    survey_key = request.form["survey_key"]

    return redirect(f"/{survey_key}/questions/0")


@app.get("/<survey_key>/questions/<int:question_id>")
def show_question(survey_key, question_id):
    """Show current question as form; redirects user to next unanswered question
    if they try to access questions out of order, or thank-you page if they've
    already completed the form, with accompanying flash messages"""

    responses = session[SESSION_RESPONSES_KEY]
    survey = surveys[survey_key]

    if len(responses) == len(survey.questions):
        flash("You've already answered all the questions!")
        return redirect(f"/{survey_key}/thanks")
    elif question_id == len(responses):
        current_question = survey.questions[question_id]
        return render_template("question.html",
                               question=current_question,
                               survey_key=survey_key)
    else:
        flash("Please answer questions in order")
        return redirect(f"/{survey_key}/questions/{len(responses)}")


@app.post("/answer")
def handle_question_submission():
    """Adds answer to session["responses"], then redirects to next question
    or thank you page if all questions have answers"""

    responses = session[SESSION_RESPONSES_KEY]
    survey_key = request.form["survey_key"]
    survey = surveys[survey_key]

    if request.form.get("answer"):
        answer = request.form["answer"]
    else:
        flash("Please choose an answer!")
        return redirect(f"/{survey_key}/questions/{len(responses)}")

    responses.append(answer)
    session[SESSION_RESPONSES_KEY] = responses

    if len(responses) == len(survey.questions):
        return redirect(f"/{survey_key}/thanks")
    else:
        return redirect(f"/{survey_key}/questions/{len(responses)}")


@app.get("/<survey_key>/thanks")
def thank_user(survey_key):
    """Displays thank you page with survey responses"""

    survey = surveys[survey_key]
    responses = session[SESSION_RESPONSES_KEY]

    return render_template("completion.html",
                           questions=survey.questions,
                           answers=responses)
