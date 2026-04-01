from flask import Blueprint, render_template, request, redirect, session
from app.models import get_user, create_user

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = get_user(request.form['username'])

        if user and user[2] == request.form['password']:
            session['user_id'] = user[0]
            session['username'] = user[1]
            return redirect('/chapters')

        return "Invalid login"

    return render_template('login.html')


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        create_user(request.form['username'], request.form['password'])
        return redirect('/login')

    return render_template('register.html')


@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect('/login')