from flask import Flask, redirect, session

def create_app():
    app = Flask(__name__)
    app.secret_key = "secret123"

    @app.route('/')
    def home_redirect():
        if 'user_id' in session:
            return redirect('/chapters')
        return redirect('/home')

    # Import and register blueprints
    from app.routes.frontend import frontend_bp
    from app.routes.auth import auth_bp
    from app.routes.chapters import chapters_bp
    from app.routes.dashboard import dashboard_bp
    from app.routes.test import test_bp

    app.register_blueprint(frontend_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(chapters_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(test_bp)

    return app