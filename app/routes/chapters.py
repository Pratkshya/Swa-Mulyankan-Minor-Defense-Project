from flask import Blueprint, render_template, session, redirect
from app.core.loader import load_chapters, get_unit_name, get_available_subjects

chapters_bp = Blueprint('chapters', __name__)

@chapters_bp.route('/chapters')
def view_subjects():
    if 'user_id' not in session:
        return redirect('/login')

    # Show the Astronomy unit overview
    try:
        chapters = load_chapters('astronomy')
        chapter_count = len(chapters)
        return render_template('unit_overview.html', 
                             unit_name='Astronomy', 
                             chapter_count=chapter_count)
    except Exception as e:
        return redirect('/login')

@chapters_bp.route('/chapters/<subject>')
def view_chapters(subject):
    if 'user_id' not in session:
        return redirect('/login')

    try:
        chapters = load_chapters(subject)
        subject_name = get_unit_name(subject)
    except Exception as e:
        # If subject not found, redirect to subject selection
        return redirect('/chapters')

    # Only return chapters with their metadata (no questions for display)
    chapter_list = [
        {
            'id': chapter['id'],
            'name': chapter['chapter_name'],
            'description': chapter['description'],
            'question_count': len(chapter.get('questions', []))
        }
        for chapter in chapters
    ]

    return render_template('chapters.html', subject=subject_name, chapters=chapter_list, subject_id=subject)
