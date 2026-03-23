from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from datetime import timedelta

db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///anchor.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = "anchor-dev-secret"
    app.config["JWT_SECRET_KEY"] = "anchor-jwt-secret"
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=30)

    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    from app.models.user import User
    from app.models.post import Post
    from app.models.comment import Comment
    from app.models.report import Report
    from app.models.resource import Resource
    
    with app.app_context():
        db.create_all()

    from app.routes.auth import auth_bp
    from app.routes.posts import posts_bp
    from app.routes.comments import comments_bp
    from app.routes.reports import reports_bp
    from app.routes.admin import admin_bp
    from app.routes.resources import resources_bp

    app.register_blueprint(auth_bp,      url_prefix="/api/auth")
    app.register_blueprint(posts_bp,     url_prefix="/api/posts")
    app.register_blueprint(comments_bp,  url_prefix="/api")
    app.register_blueprint(reports_bp,   url_prefix="/api/reports")
    app.register_blueprint(admin_bp,     url_prefix="/api/admin")
    app.register_blueprint(resources_bp,   url_prefix="/api/resources")

    @app.route("/")
    def home():
        return {"message": "ANCHOR API is running 🎉"}

    return app