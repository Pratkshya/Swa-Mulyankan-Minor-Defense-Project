from flask import Blueprint, render_template

frontend_bp = Blueprint('frontend', __name__)

@frontend_bp.route('/')
def home():
    """Home page"""
    return render_template('home.html')

@frontend_bp.route('/home')
def home_page():
    """Home page (alternate route)"""
    return render_template('home.html')

@frontend_bp.route('/features')
def features():
    """Features page"""
    return render_template('features.html')

@frontend_bp.route('/about')
def about():
    """About page"""
    return render_template('about.html')
