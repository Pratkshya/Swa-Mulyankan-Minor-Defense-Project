from flask import Blueprint, render_template, session, redirect
from app.core.loader import load_chapters, get_unit_name, get_available_subjects

chapters_bp = Blueprint('chapters', __name__)

@chapters_bp.route('/chapters')
def view_subjects():
    if 'user_id' not in session:
        return redirect('/login')

    # Load all available subjects
    subjects = []
    subject_info = {
        'astronomy': {'icon': '🌌', 'description': 'Explore the cosmos, planets, and stars'},
        'physics': {'icon': '⚡', 'description': 'Study forces, energy, and motion'},
        'biology': {'icon': '🧬', 'description': 'Learn life science, cells, and ecosystems'},
        'chemistry': {'icon': '🧪', 'description': 'Understand atoms, reactions, and chemical principles'}
    }
    
    try:
        available = get_available_subjects()
        for subject in available:
            chapters = load_chapters(subject)
            subject_name = get_unit_name(subject)
            info = subject_info.get(subject, {'icon': '📖', 'description': ''})
            subjects.append({
                'id': subject,
                'name': subject_name,
                'icon': info['icon'],
                'description': info['description'],
                'chapter_count': len(chapters)
            })
    except Exception as e:
        return redirect('/login')
    
    # If only one subject, show that one; otherwise show selection
    if len(subjects) == 1:
        return render_template('unit_overview.html', 
                             unit_name=subjects[0]['name'], 
                             chapter_count=subjects[0]['chapter_count'])
    else:
        return render_template('subjects.html', subjects=subjects)

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
