from flask import Blueprint, render_template
from models.quiz_model import Quiz

quiz = Blueprint('quiz', __name__, url_prefix='/quiz')

@quiz.route('/')
def index():
    quizzes = Quiz.query.all()
    return render_template('quiz/index.html', quizzes=quizzes)

@quiz.route('/<int:id>')
def quiz_detail(id):
    quiz = Quiz.query.get_or_404(id)
    return render_template('quiz/quiz_detail.html', quiz=quiz)
