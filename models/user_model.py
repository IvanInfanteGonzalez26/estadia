from .db_config import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.Text)
    role = db.Column(db.String(50), nullable=False)
    
    VALID_ROLES = {"instructor_profesores", "instructor_estudiantes", "profesor", "estudiante"}
    
    def __init__(self, username, password, role) -> None:
        if role not in self.VALID_ROLES:
            raise ValueError(f"Rol no válido: {role}")
        
        self.username = username
        self.password = password
        self.role = role

    def __repr__(self) -> str:
        return f'User: {self.username}'

