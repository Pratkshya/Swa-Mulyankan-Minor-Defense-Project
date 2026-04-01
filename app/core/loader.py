import json
import os


def _load_spec_data(subject=None):
    """
    Load data from the subject-specific JSON file.
    If subject is None, defaults to 'astronomy' (cdc_specification.json)
    If subject is 'astronomy', loads cdc_specification.json
    If subject is 'physics', loads physics_specification.json
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    # Map subject names to file names
    subject_files = {
        'astronomy': 'cdc_specification.json',
        'physics': 'physics_specification.json'
    }

    # Default to astronomy if no subject specified
    if subject is None:
        subject = 'astronomy'

    subject = subject.lower()
    if subject not in subject_files:
        raise ValueError(f"Unknown subject: {subject}. Supported subjects: astronomy, physics")

    json_path = os.path.join(base_dir, 'data', subject_files[subject])

    if not os.path.exists(json_path):
        raise FileNotFoundError(f"Subject specification file not found: {json_path}")

    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if isinstance(data, dict) and 'chapters' in data:
                return data
            else:
                raise ValueError(f"Invalid JSON structure in {json_path}: expected 'chapters' key")
    except json.JSONDecodeError as e:
        raise json.JSONDecodeError(f"Invalid JSON in {json_path}: {e}")
    except OSError as e:
        raise OSError(f"Error reading {json_path}: {e}")


def load_chapters(subject=None):
    """
    Load all chapters from the subject-specific JSON file.
    Returns the chapters array with chapter metadata and questions.
    """
    data = _load_spec_data(subject)
    return data['chapters']


def load_questions(subject=None):
    """
    Load questions data from the subject-specific JSON file.
    Returns a list of chapters (same as load_chapters) for compatibility.
    """
    data = _load_spec_data(subject)
    if isinstance(data, dict) and 'chapters' in data:
        return data['chapters']
    return []


def get_chapter_by_id(chapter_id, subject=None):
    """
    Get a specific chapter by its ID from the subject-specific file.
    Returns the chapter object with all its questions.
    """
    chapters = load_chapters(subject)
    for chapter in chapters:
        if chapter.get('id') == chapter_id:
            return chapter
    return None


def get_questions_for_chapter(chapter_id, subject=None):
    """
    Get questions for a specific chapter from the subject-specific file.
    Returns the questions array for the given chapter ID.
    """
    chapter = get_chapter_by_id(chapter_id, subject)
    if chapter and 'questions' in chapter:
        return chapter['questions']
    return []


def get_unit_name(subject=None):
    """
    Get the subject/unit name from the subject-specific JSON file.
    """
    try:
        data = _load_spec_data(subject)
        if isinstance(data, dict) and 'subject' in data:
            return data['subject']
        return "Unknown Subject"
    except Exception:
        return "Unknown Subject"


def get_available_subjects():
    """
    Get list of available subjects based on existing JSON files.
    Returns a list of subject names that have corresponding JSON files.
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    subjects = []

    # Check for astronomy file
    astronomy_path = os.path.join(base_dir, 'data', 'cdc_specification.json')
    if os.path.exists(astronomy_path):
        subjects.append('astronomy')

    # Check for physics file
    physics_path = os.path.join(base_dir, 'data', 'physics_specification.json')
    if os.path.exists(physics_path):
        subjects.append('physics')

    return subjects

