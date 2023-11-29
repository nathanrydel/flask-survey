from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

SESSION_RESPONSES_KEY = "responses"

#TODO: Change root directory to a survey menu
#TODO: Handle submission to pick the survey, submit to next page
#TODO: Move show_survey_home() view function to a new endpoint
#TODO: Add survey variables to all non-root endpoints for tracking


@app.get("/")
def show_survey_home():
    """Show survey title, instructions, and a button. Clears
    session["responses"] on page load"""

    # session["responses"] = []

    return render_template("survey_start.html", survey=survey)


@app.post("/begin")
def start_survey():
    """Start the survey"""

    # putting in the show function to clear everytime home page renders
    session[SESSION_RESPONSES_KEY] = []

    return redirect("/questions/0")


@app.get("/questions/<int:question_id>")
def show_question(question_id):
    """Show current question as form; redirects user to next unanswered question
    if they try to access questions out of order, or thank-you page if they've
    already completed the form, with accompanying flash messages"""

    responses = session[SESSION_RESPONSES_KEY]

    if len(responses) == len(survey.questions):
        flash("You've already answered all the questions!")
        return redirect("/thanks")
    elif question_id == len(responses):
        current_question = survey.questions[question_id]
        return render_template("question.html", question=current_question)
    else:
        flash("Please answer questions in order")
        return redirect(f"/questions/{len(responses)}")


@app.post("/answer")
def handle_question_submission():
    """Adds answer to session["responses"], then redirects to next question
    or thank you page if all questions have answers"""

    responses = session[SESSION_RESPONSES_KEY]

    if request.form.get("answer"):
        answer = request.form["answer"]
    else:
        flash("Please choose an answer!")
        return redirect(f"/questions/{len(responses)}")

    responses.append(answer)
    session[SESSION_RESPONSES_KEY] = responses

    if len(responses) == len(survey.questions):
        return redirect("/thanks")
    else:
        return redirect(f"/questions/{len(responses)}")


@app.get("/thanks")
def thank_user():
    """Displays thank you page with survey responses"""

    responses = session[SESSION_RESPONSES_KEY]

    return render_template("completion.html",
                           questions=survey.questions,
                           answers=responses)
