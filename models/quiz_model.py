from .db_config import db

class Quiz(db.Model):
    __tablename__ = 'quizzes'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # 📌 Nuevo campo
    question = db.Column(db.Text, nullable=False)
    option_a = db.Column(db.String(255), nullable=False)
    option_b = db.Column(db.String(255), nullable=False)
    option_c = db.Column(db.String(255), nullable=False)
    option_d = db.Column(db.String(255), nullable=False)
    correct_answer = db.Column(db.String(255), nullable=False)

    def __init__(self, title, creator_id, question, option_a, option_b, option_c, option_d, correct_answer):
        self.title = title
        self.creator_id = creator_id  # 📌 Guardar quién lo creó
        self.question = question
        self.option_a = option_a
        self.option_b = option_b
        self.option_c = option_c
        self.option_d = option_d
        self.correct_answer = correct_answer

class StudentAttempt(db.Model):
    __tablename__ = 'student_attempts'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.id'), nullable=False)
    score = db.Column(db.Float, nullable=False)  # 🔹 Puntaje obtenido

    def __init__(self, student_id, quiz_id, score):
        self.student_id = student_id
        self.quiz_id = quiz_id
        self.score = score
