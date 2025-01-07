from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models import db, Subject, Chapter, Quiz, Degree, User
from functools import wraps

admin = Blueprint('admin', __name__)

# Admin required decorator
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in first.', 'error')
            return redirect(url_for('auth.login'))
        user = User.query.get(session['user_id'])
        if not user or not user.is_admin:
            flash('Admin access required.', 'error')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@admin.route('/admin/dashboard')
@admin_required
def dashboard():
    subjects = Subject.query.all()
    degrees = Degree.query.all()
    return render_template('admin/dashboard.html', subjects=subjects, degrees=degrees)

@admin.route('/admin/add_subject', methods=['POST'])
@admin_required
def add_subject():
    subject_name = request.form.get('subject_name')
    degree_id = request.form.get('degree_id')
    
    if subject_name and degree_id:
        subject = Subject(subject=subject_name, degree_id=degree_id)
        db.session.add(subject)
        db.session.commit()
        flash('Subject added successfully!', 'success')
    return redirect(url_for('admin.dashboard'))

@admin.route('/admin/add_chapter', methods=['POST'])
@admin_required
def add_chapter():
    chapter_name = request.form.get('chapter_name')
    subject_id = request.form.get('subject_id')
    
    if chapter_name and subject_id:
        chapter = Chapter(chapter_name=chapter_name, subject_id=subject_id)
        db.session.add(chapter)
        db.session.commit()
        flash('Chapter added successfully!', 'success')
    return redirect(url_for('admin.dashboard'))

@admin.route('/admin/add_quiz', methods=['POST'])
@admin_required
def add_quiz():
    quiz_name = request.form.get('quiz_name')
    chapter_id = request.form.get('chapter_id')
    
    if quiz_name and chapter_id:
        quiz = Quiz(quiz_name=quiz_name, chapter_id=chapter_id)
        db.session.add(quiz)
        db.session.commit()
        flash('Quiz added successfully!', 'success')
    return redirect(url_for('admin.dashboard'))

@admin.route('/admin/get_chapters/<subject_id>')
@admin_required
def get_chapters(subject_id):
    chapters = Chapter.query.filter_by(subject_id=subject_id).all()
    return render_template('admin/chapters_table.html', chapters=chapters)

@admin.route('/admin/get_quizzes/<chapter_id>')
@admin_required
def get_quizzes(chapter_id):
    quizzes = Quiz.query.filter_by(chapter_id=chapter_id).all()
    return render_template('admin/quizzes_modal.html', quizzes=quizzes, chapter_id=chapter_id)