from flask import Blueprint, request, render_template, redirect, session
import json
from app.core.analyzer import analyze
from app.core.loader import get_questions_for_chapter
from app.models import save_result

test_bp = Blueprint('test', __name__)

@test_bp.route('/submit', methods=['POST'])
def submit():
    if 'user_id' not in session:
        return redirect('/login')

    chapter_id = session.get('current_chapter_id')
    subject = session.get('current_subject', 'astronomy')
    if not chapter_id:
        return redirect('/chapters')

    questions = get_questions_for_chapter(chapter_id, subject)

    # Get answers from form data
    answers = {}
    for question in questions:
        answer = request.form.get(str(question['id']))
        if answer:
            answers[str(question['id'])] = answer

    # Get attempts data
    attempts_data_str = request.form.get('attempts_data', '{}')
    try:
        attempts_data = json.loads(attempts_data_str)
    except json.JSONDecodeError:
        attempts_data = {}

    # Analyze the quiz results
    result = analyze(answers, questions, attempts_data)

    # Save result to database
    save_result(session['user_id'], result['mastery'], result['gap'], result['status'])

    return render_template(
        'result.html',
        mastery=result['mastery'],
        gap=result['gap'],
        status=result['status'],
        heatmap=result['heatmap'],
        plan=result['plan'],
        severity_analysis=result.get('severity_analysis', {})
    )
