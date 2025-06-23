from flask import Flask
from app.routes import routes_bp
from app.auth import auth_bp
from app.database import db




def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "sdsdsdsdSERER#$#$EDtfrrdesswsdfghhgf"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///pharma.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    app.register_blueprint(routes_bp)
    app.register_blueprint(auth_bp)
    return app
app = create_app()