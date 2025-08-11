from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
from flask_session import Session

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.secret_key = 'My_secret_key'
    app.config["SESSION_TYPE"] = "filesystem"
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=1)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///forumdb.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    Session(app)
    
    db.init_app(app)

    from .main import main
    from .api import api
    app.register_blueprint(main)
    app.register_blueprint(api, url_prefix="/api")

    with app.app_context():
        db.create_all()

    # ✅ Register 404 handler AFTER app is created
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template("404.html"), 404

    return app
