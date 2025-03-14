from flask import Blueprint, render_template, request, redirect, url_for, flash, g
from models.db_config import db
from models.quiz_model import Quiz, StudentAttempt
from models.user_model import User
from controllers.auth_controller import login_required
import random

quiz = Blueprint('quiz', __name__, url_prefix='/quiz')

@quiz.route('/')
@login_required
def index():
    # 🔹 Obtener los títulos únicos de los exámenes
    quiz_titles = db.session.query(Quiz.title).distinct().all()

    return render_template('quiz/index.html', quizzes=[title[0] for title in quiz_titles])


# ✅ **Ruta para que los instructores creen exámenes**
@quiz.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if g.user.role not in ['instructor_profesores', 'instructor_estudiantes']:
        flash("No tienes permisos para crear exámenes.")
        return redirect(url_for('quiz.index'))

    if request.method == 'POST':
        title = request.form.get('title')
        questions = request.form.getlist('question')
        options_a = request.form.getlist('option_a')
        options_b = request.form.getlist('option_b')
        options_c = request.form.getlist('option_c')
        options_d = request.form.getlist('option_d')
        correct_answers = request.form.getlist('correct_answer')

        # Guardar cada pregunta en la base de datos
        for i in range(len(questions)):
            new_question = Quiz(
                title=title,
                question=questions[i],
                option_a=options_a[i],
                option_b=options_b[i],
                option_c=options_c[i],
                option_d=options_d[i],
                correct_answer=correct_answers[i],
                author_id=g.user.id
            )
            db.session.add(new_question)
        
        db.session.commit()
        flash("Examen creado exitosamente.")
        return redirect(url_for('quiz.index'))

    return render_template('quiz/create.html')

@quiz.route('/delete/<string:title>', methods=['POST'])
@login_required
def delete(title):
    if g.user.role not in ['instructor_profesores', 'instructor_estudiantes']:
        flash("No tienes permisos para eliminar exámenes.")
        return redirect(url_for('quiz.index'))

    # Borrar todas las preguntas relacionadas con el título del examen
    Quiz.query.filter_by(title=title).delete()
    db.session.commit()
    
    flash("Examen eliminado correctamente.")
    return redirect(url_for('quiz.index'))

@quiz.route('/attempt/<string:title>', methods=['GET', 'POST'])
@login_required
def attempt_quiz(title):
    if g.user.role not in ['profesor', 'estudiante']:
        flash("No tienes permisos para realizar exámenes.")
        return redirect(url_for('quiz.index'))

    # Verificar si ya hizo el examen
    existing_attempt = StudentAttempt.query.filter_by(student_id=g.user.id, quiz_id=title).first()
    if existing_attempt:
        flash("Ya has realizado este examen.")
        return redirect(url_for('quiz.index'))

    questions = Quiz.query.filter_by(title=title).all()
    
    if request.method == 'POST':
        score = 0
        total_questions = len(questions)

        for question in questions:
            user_answer = request.form.get(f'question_{question.id}')
            if user_answer == question.correct_answer:
                score += 1
        
        final_score = (score / total_questions) * 100

        # Guardar el intento
        attempt = StudentAttempt(student_id=g.user.id, quiz_id=title, score=final_score)
        db.session.add(attempt)
        db.session.commit()

        flash(f"Examen completado. Tu puntaje: {final_score}%")
        return redirect(url_for('quiz.index'))

    # Mezclar preguntas en orden aleatorio
    random.shuffle(questions)

    return render_template('quiz/attempt.html', title=title, questions=questions)
