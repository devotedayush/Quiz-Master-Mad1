from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Date, Time
db = SQLAlchemy()

# models.py
class User(db.Model):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(90), unique=True, nullable=False)  # Fixed typo "Coulumn" to "Column"
    password = db.Column(db.String(255), nullable=False)  # Increased length for hashed passwords
    full_name = db.Column(db.String(30), nullable=False)
    dob = db.Column(db.Date, nullable=True)
    degree_id = db.Column(db.Integer, db.ForeignKey('degree_level.degree_id'))
    is_admin = db.Column(db.Boolean, nullable=False, default=False)  # Fixed "db.column" to "db.Column"

    # Relationships
    degree = db.relationship('Degree_level', backref=db.backref('users', lazy=True))

    def set_password(self, password):
        # Implement password hashing logic here, e.g., using werkzeug.security
        from werkzeug.security import generate_password_hash
        self.password = generate_password_hash(password)

def create_admin_if_not_exists():
    admin = User.query.filter_by(email="admin@gmail.com").first()
    if not admin:
        admin = User(
            full_name="admin",
            email="admin@gmail.com",
            username="admin",
            is_admin=True
        )
        admin.set_password("admin")
        db.session.add(admin)
        db.session.commit()
        print("Admin user created successfully")

class Degree_level(db.Model):
    __tablename__ = 'degree_level'
    degree_id = db.Column(db.Integer, primary_key=True)
    degree_level = db.Column(db.String(10), unique=True, nullable=False)

class Subject(db.Model):
    __tablename__ = 'subjects'
    subject_id = db.Column(db.Integer, primary_key=True)
    subject_name = db.Column(db.String(20), nullable=False)
    degree_id = db.Column(db.Integer, db.ForeignKey('degree_level.degree_id'))

    # Relationships
    degree = db.relationship('Degree_level', backref=db.backref('subjects', lazy=True))
    #subjects.chapters
    chapters = db.relationship('Chapter', backref=db.backref('subject', lazy=True))

class Chapter(db.Model):
    __tablename__ = 'chapters'
    chapter_id = db.Column(db.Integer, primary_key=True)
    chapter_name = db.Column(db.String(20), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.subject_id'))

    # Relationships
    quizzes = db.relationship('Quiz', backref=db.backref('chapter', lazy=True))

class Quiz(db.Model):
    __tablename__ = 'quiz'
    quiz_id = db.Column(db.Integer, primary_key=True)
    quiz_name = db.Column(db.String(50), nullable=False)
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapters.chapter_id'))

    # Relationships
    questions = db.relationship('Question', backref='quiz', cascade='all, delete-orphan')
    
class Question(db.Model):
    __tablename__ = 'questions'
    question_id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text, nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.quiz_id'))

    # Relationships question.options
    options = db.relationship('Option', backref='question', cascade='all, delete-orphan')
class Option(db.Model):
    __tablename__ = 'options'
    option_id = db.Column(db.Integer, primary_key=True)
    option_text = db.Column(db.Text, nullable=False)  # THIS WAS MISSING
    is_correct = db.Column(db.Boolean, nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.question_id'))

class Quiz_Attempt(db.Model):
    __tablename__ = 'quiz_attempts'
    quiz_attempt_id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.quiz_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    date_of_attempt = db.Column(db.Date, nullable=False)  # Use db.Date
    duration_of_attempt = db.Column(db.Time, nullable=False)  # Use db.Time
    quiz_score = db.Column(db.Integer, nullable=False)  # Fix db.column typo

    # Relationships user.quiz_attempts
    user = db.relationship('User', backref=db.backref('quiz_attempts', lazy=True))  # Link to User
    # quiz.quiz_attempts returns a list of objects
    quiz = db.relationship('Quiz', backref=db.backref('quiz_attempts', lazy=True))  # Link to Quiz

