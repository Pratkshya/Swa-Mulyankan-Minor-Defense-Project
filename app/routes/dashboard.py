from flask import Blueprint, render_template, session, redirect, request
import random
from app.core.loader import load_chapters, get_questions_for_chapter, get_chapter_by_id

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/quiz/<int:chapter_id>')
def quiz(chapter_id):
    if 'user_id' not in session:
        return redirect('/login')

    # Get subject from query parameter, default to astronomy
    subject = request.args.get('subject', 'astronomy')

    chapter = get_chapter_by_id(chapter_id, subject)
    if not chapter:
        return redirect('/chapters')

    questions = get_questions_for_chapter(chapter_id, subject)

    # Limit to 15 random questions and shuffle them
    if len(questions) > 15:
        questions = random.sample(questions, 15)
    else:
        # Shuffle if we have 15 or less
        questions = questions.copy()
        random.shuffle(questions)

    # Store in session for submission
    session['current_chapter_id'] = chapter_id
    session['current_subject'] = subject
    session['current_questions'] = [q['id'] for q in questions]
    session.modified = True

    return render_template(
        'quiz.html',
        chapter_name=chapter['chapter_name'],
        chapter_id=chapter_id,
        subject=subject,
        questions=questions
    )