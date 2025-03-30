from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models import db, User, Degree_level, Subject, Chapter, Quiz, Question, Option, Quiz_Attempt
from functools import wraps
import datetime
from sqlalchemy import or_

user = Blueprint('user', __name__)

# Simple login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in first.', 'error')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@user.route('/dashboard')
@login_required
def dashboard():
    user_obj = User.query.get(session['user_id'])
    search_query = request.args.get('search_query', '')

    # Query quizzes available for the user's degree level
    quizzes_query = Quiz.query.join(Chapter).join(Subject).filter(Subject.degree_id == user_obj.degree_id)
    if search_query:
        quizzes_query = quizzes_query.filter(
            or_(
                Quiz.quiz_name.ilike(f'%{search_query}%'),
                Chapter.chapter_name.ilike(f'%{search_query}%'),
                Subject.subject_name.ilike(f'%{search_query}%')
            )
        )
    quizzes = quizzes_query.all()
    return render_template('user/dashboard.html', quizzes=quizzes, search_query=search_query, user_obj=user_obj)

@user.route('/quiz_info/<int:quiz_id>')
@login_required
def quiz_info(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    return render_template('user/quiz_info.html', quiz=quiz)

@user.route('/take_quiz/<int:quiz_id>', methods=['GET'])
@login_required
def take_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    # Record the start time (as ISO formatted string) in the session
    session['quiz_start_time'] = datetime.datetime.now().isoformat()
    return render_template('user/take_quiz.html', quiz=quiz)

@user.route('/submit_quiz/<int:quiz_id>', methods=['POST'])
@login_required
def submit_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    # Retrieve the start time from the session
    start_time_str = session.pop('quiz_start_time', None)
    if start_time_str:
        start_time = datetime.datetime.fromisoformat(start_time_str)
    else:
        start_time = datetime.datetime.now()  # fallback

    end_time = datetime.datetime.now()
    duration = end_time - start_time
    # Convert duration (timedelta) to a time object (assuming duration is less than 24 hours)
    duration_time = (datetime.datetime.min + duration).time()

    score = 0
    total_questions = len(quiz.questions)
    # Iterate over each question and check the selected answer
    for question in quiz.questions:
        selected_option_id = request.form.get(f'question_{question.question_id}')
        if selected_option_id:
            option = Option.query.get(int(selected_option_id))
            if option and option.is_correct:
                score += 1

    # Save the quiz attempt
    attempt = Quiz_Attempt(
        quiz_id=quiz.quiz_id,
        user_id=session['user_id'],
        date_of_attempt=datetime.date.today(),
        duration_of_attempt=duration_time,
        quiz_score=score
    )
    db.session.add(attempt)
    db.session.commit()

    flash(f'You scored {score} out of {total_questions}', 'success')
    return render_template('user/quiz_result.html', score=score, total_questions=total_questions, attempt=attempt)

@user.route('/quiz_summary')
@login_required
def quiz_summary():
    attempts = Quiz_Attempt.query.filter_by(user_id=session['user_id']).order_by(Quiz_Attempt.quiz_attempt_id.desc()).all()
    return render_template('user/quiz_summary.html', attempts=attempts)
