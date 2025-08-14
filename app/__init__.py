from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
import os

db = SQLAlchemy()
jwt = JWTManager()

def create_app():
    load_dotenv()
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///forumdb.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
        # ---- JWT config ----
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'dev-change-me')
    app.config['JWT_ACCESS_TOKEN_EXPIRES']  = timedelta(minutes=int(os.getenv('JWT_ACCESS_MINUTES', 15)))
    app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=int(os.getenv('JWT_REFRESH_DAYS', 7)))

    db.init_app(app)
    jwt.init_app(app)

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
