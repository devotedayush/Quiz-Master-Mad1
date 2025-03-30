from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models import db, Subject, Chapter, Quiz, Degree_level, User, Question, Option, Quiz_Attempt
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

@admin.route('/dashboard')
@admin_required
def dashboard():
    subjects = Subject.query.all()
    degrees = Degree_level.query.all()
    return render_template('admin/dashboard.html', subjects=subjects, degrees=degrees)

@admin.route('/add_subject', methods=['POST'])
@admin_required
def add_subject():
    subject_name = request.form.get('subject_name')
    degree_id = request.form.get('degree_id')
    if subject_name and degree_id:
        subject = Subject(subject_name=subject_name, degree_id=degree_id)
        db.session.add(subject)
        db.session.commit()
        flash('Subject added successfully!', 'success')
    return redirect(url_for('admin.dashboard'))

@admin.route('/get_chapters', methods=['GET', 'POST'])
@admin_required
def get_chapters():
    subject_id = request.args.get('subject_id') if request.method == 'GET' else request.form.get('subject_id')
    current_subject = Subject.query.filter_by(subject_id=subject_id).first()
    chapters = Chapter.query.filter_by(subject_id=subject_id).all() or []
    return render_template('admin/view_chapters.html', chapters=chapters, current_subject=current_subject)

@admin.route('/add_chapter', methods=['POST'])
@admin_required
def add_chapter():
    chapter_name = request.form.get('chapter_name')
    subject_id = request.form.get('subject_id')
    if chapter_name and subject_id:
        chapter = Chapter(chapter_name=chapter_name, subject_id=subject_id)
        db.session.add(chapter)
        db.session.commit()
        flash('Chapter added successfully!', 'success')
    return redirect(url_for('admin.get_chapters', subject_id=subject_id))

@admin.route('/delete_chapter', methods=['POST'])
@admin_required
def delete_chapter():
    chapter_id = request.form.get('chapter_id')
    chapter = Chapter.query.get(chapter_id)
    if chapter:
        subject_id = chapter.subject_id
        db.session.delete(chapter)
        db.session.commit()
    return redirect(url_for('admin.get_chapters', subject_id=subject_id))

@admin.route('/admin/get_quizzes', methods=['GET', 'POST'])
@admin_required
def get_quizzes():
    chapter_id = request.args.get('chapter_id') if request.method == 'GET' else request.form.get('chapter_id')
    chapter = Chapter.query.get(chapter_id)
    quizzes = chapter.quizzes if chapter else []
    return render_template('admin/view_quizzes.html', quizzes=quizzes, chapter_id=chapter_id, chapter=chapter)

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
    return redirect(url_for('admin.get_quizzes', chapter_id=chapter_id))

@admin.route('/admin/delete_quiz', methods=['POST'])
@admin_required
def delete_quiz():
    quiz_id = request.form.get('quiz_id')
    quiz = Quiz.query.get(quiz_id)
    if quiz:
        chapter_id = quiz.chapter_id
        db.session.delete(quiz)
        db.session.commit()
    return redirect(url_for('admin.get_quizzes', chapter_id=chapter_id))

@admin.route('/admin/get_questions', methods=['GET', 'POST'])
@admin_required
def get_questions():
    quiz_id = request.args.get('quiz_id') if request.method == 'GET' else request.form.get('quiz_id')
    quiz = Quiz.query.get(quiz_id)
    questions = quiz.questions if quiz else []
    return render_template('admin/view_questions.html', questions=questions, quiz_id=quiz_id, quiz=quiz)
@admin.route('/admin/add_question', methods=['POST', 'GET'])
@admin_required
def add_question():
    if request.method == 'POST':
        question_text = request.form.get('question')
        quiz_id = request.form.get('quiz_id')
        correct_option = request.form.get('correct_option')
        
        if question_text and quiz_id and correct_option is not None:
            correct_option = int(correct_option)
            
            # Create and save the question
            question = Question(question=question_text, quiz_id=quiz_id)
            db.session.add(question)
            db.session.commit()
            
            # Get the option texts
            options = []
            for i in range(4):  # 4 options
                # Changed this line to match the form field name
                option_text = request.form.get(f'options[{i}][option_text]')
                is_correct = (i == correct_option)
                if option_text:
                    options.append(Option(
                        question_id=question.question_id,
                        option_text=option_text,  # Changed this to match your model field
                        is_correct=is_correct
                    ))
            
            if options:
                db.session.add_all(options)
                db.session.commit()
                flash('Question and options added successfully!', 'success')
            else:
                flash('No valid options provided.', 'danger')
                db.session.delete(question)
                db.session.commit()
                
            return redirect(url_for('admin.get_questions', quiz_id=quiz_id))
        else:
            flash('Please fill out all fields and select the correct answer.', 'danger')
            return redirect(url_for('admin.get_questions', quiz_id=quiz_id))

    # GET request
    quiz_id = request.args.get('quiz_id')
    if quiz_id:
        quiz = Quiz.query.get(quiz_id)
        questions = quiz.questions if quiz else []
        return render_template('admin/view_questions.html', quiz_id=quiz_id, quiz=quiz, questions=questions)
    else:
        flash('Quiz ID is required.', 'danger')
        return redirect(url_for('admin.dashboard'))


@admin.route('/admin/delete_question', methods=['POST'])
@admin_required
def delete_question():
    question_id = request.form.get('question_id')
    question = Question.query.get(question_id)
    if question:
        quiz_id = question.quiz_id
        db.session.delete(question)
        db.session.commit()
    return redirect(url_for('admin.get_questions', quiz_id=quiz_id))
@admin.route('/add_degree', methods=['POST'])
@admin_required
def add_degree():
    degree_level = request.form.get('degree_level')
    if degree_level:
        # Check if degree level already exists
        existing_degree = Degree_level.query.filter_by(degree_level=degree_level).first()
        if existing_degree:
            flash('This degree level already exists!', 'error')
        else:
            new_degree = Degree_level(degree_level=degree_level)
            db.session.add(new_degree)
            db.session.commit()
            flash('Degree level added successfully!', 'success')
    else:
        flash('Degree level name is required!', 'error')
    return redirect(url_for('admin.dashboard'))

@admin.route('/edit_degree', methods=['POST'])
@admin_required
def edit_degree():
    degree_id = request.form.get('degree_id')
    degree_name = request.form.get('degree_name')
    
    if degree_id and degree_name:
        degree = Degree_level.query.get(degree_id)
        if degree:
            # Check if the new name already exists (excluding the current degree)
            existing = Degree_level.query.filter(
                Degree_level.degree_level == degree_name,
                Degree_level.degree_id != degree_id
            ).first()
            
            if existing:
                flash('This degree level name already exists!', 'error')
            else:
                degree.degree_level = degree_name
                db.session.commit()
                flash('Degree level updated successfully!', 'success')
        else:
            flash('Degree level not found!', 'error')
    else:
        flash('Missing required information!', 'error')
    return redirect(url_for('admin.dashboard'))

@admin.route('/delete_degree', methods=['POST'])
@admin_required
def delete_degree():
    degree_id = request.form.get('degree_id')
    if degree_id:
        degree = Degree_level.query.get(degree_id)
        if degree:
            # Check if there are subjects associated with this degree
            subjects = Subject.query.filter_by(degree_id=degree_id).all()
            if subjects:
                # Delete all associated subjects and their chapters
                for subject in subjects:
                    # Delete chapters associated with this subject
                    chapters = Chapter.query.filter_by(subject_id=subject.subject_id).all()
                    for chapter in chapters:
                        # Delete quizzes associated with this chapter
                        quizzes = Quiz.query.filter_by(chapter_id=chapter.chapter_id).all()
                        for quiz in quizzes:
                            # Delete questions and options associated with this quiz
                            questions = Question.query.filter_by(quiz_id=quiz.quiz_id).all()
                            for question in questions:
                                # Delete options associated with this question
                                Option.query.filter_by(question_id=question.question_id).delete()
                            # Delete questions
                            Question.query.filter_by(quiz_id=quiz.quiz_id).delete()
                        # Delete quizzes
                        Quiz.query.filter_by(chapter_id=chapter.chapter_id).delete()
                    # Delete chapters
                    Chapter.query.filter_by(subject_id=subject.subject_id).delete()
                # Delete subjects
                Subject.query.filter_by(degree_id=degree_id).delete()
            
            # Finally delete the degree
            db.session.delete(degree)
            db.session.commit()
            flash('Degree level and all associated data deleted successfully!', 'success')
        else:
            flash('Degree level not found!', 'error')
    else:
        flash('Degree ID is required!', 'error')
    return redirect(url_for('admin.dashboard'))

@admin.route('/analytics')
@admin_required
def analytics():
    # Get total counts
    total_users = User.query.filter_by(is_admin=False).count()
    total_quizzes = Quiz.query.count()
    total_attempts = Quiz_Attempt.query.count()
    
    # Calculate average score
    avg_score = db.session.query(db.func.avg(Quiz_Attempt.quiz_score)).scalar() or 0
    avg_score = round(avg_score, 2)
    
    # Get most popular quizzes (top 5)
    popular_quizzes = db.session.query(
        Quiz.quiz_name, db.func.count(Quiz_Attempt.quiz_attempt_id).label('attempts')
    ).join(Quiz_Attempt, Quiz.quiz_id == Quiz_Attempt.quiz_id) \
     .group_by(Quiz.quiz_id) \
     .order_by(db.desc('attempts')) \
     .limit(5).all()
    
    # Get quiz performance data for the chart
    quiz_data = db.session.query(
        Quiz.quiz_name,
        db.func.count(Quiz_Attempt.quiz_attempt_id).label('attempts'),
        db.func.avg(Quiz_Attempt.quiz_score).label('average_score')
    ).join(Quiz_Attempt, Quiz.quiz_id == Quiz_Attempt.quiz_id) \
     .group_by(Quiz.quiz_id) \
     .limit(5).all()
    
    # Prepare data for charts
    quiz_names = [quiz[0] for quiz in quiz_data]
    quiz_attempts = [int(quiz[1]) for quiz in quiz_data]
    quiz_scores = [float(quiz[2] or 0) for quiz in quiz_data]
    
    return render_template(
        'admin/analytics.html',
        total_users=total_users,
        total_quizzes=total_quizzes,
        total_attempts=total_attempts,
        avg_score=avg_score,
        popular_quizzes=popular_quizzes,
        quiz_names=quiz_names,
        quiz_attempts=quiz_attempts,
        quiz_scores=quiz_scores
    )

