from flask import Blueprint, render_template
from models.db_config import db
from models.quiz_model import Quiz
from controllers.auth_controller import login_required

quiz = Blueprint('quiz', __name__, url_prefix='/quiz')

@quiz.route('/')
@login_required
def index():
    # Obtener solo los títulos únicos de los quizzes
    quiz_titles = db.session.query(Quiz.title).distinct().all()
    return render_template('quiz/index.html', quizzes=[title[0] for title in quiz_titles])

# NUEVA RUTA PARA VER PREGUNTAS DE UN QUIZ
@quiz.route('/view/<string:title>')
@login_required
def view_quiz(title):
    # Filtra las preguntas según el título del quiz
    questions = Quiz.query.filter_by(title=title).all()
    return render_template('quiz/view.html', title=title, questions=questions)
