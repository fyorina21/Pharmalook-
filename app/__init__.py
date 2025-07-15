# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from app.routes import routes_bp
# from app.auth import auth_bp
# from app.database import db
# from flask_migrate import Migrate

# db = SQLAlchemy()
# migrate = Migrate()






# def create_app():
#     app = Flask(__name__)
#     app.config["SECRET_KEY"] = "sdsdsdsdSERER#$#$EDtfrrdesswsdfghhgf"
#     app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///pharma.db"
#     app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False   
#     db.init_app(app)
#     app.register_blueprint(routes_bp)
#     app.register_blueprint(auth_bp)
#     db.init_app(app)
#     migrate.init_app(app, db)


#     return app
# app = create_app()



from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from app.routes import routes_bp
from app.auth import auth_bp
from app.database import db  # already contains: db = SQLAlchemy()
# from flask_login import LoginManager

# login_manager = LoginManager()

migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "sdsdsdsdSERER#$#$EDtfrrdesswsdfghhgf"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///pharma.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False   
    
    db.init_app(app)
    migrate.init_app(app, db)
    # login_manager.init_app(app) 

    app.register_blueprint(routes_bp)
    app.register_blueprint(auth_bp)

    return app

app = create_app()
