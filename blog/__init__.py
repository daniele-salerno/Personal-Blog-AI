from flask import Flask

from flask_sqlalchemy import SQLAlchemy 
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_misaka import Misaka

from config import Config
from flask_mongoengine import MongoEngine

app = Flask(__name__)
app.config.from_object(Config)

# db = SQLAlchemy(app)
# migrate = Migrate(app, db)
db = MongoEngine()
db.init_app(app)

login_manager = LoginManager(app)
Misaka(app)

# with app.app_context():
#     if db.engine.url.drivername == 'sqlite':
#         migrate.init_app(app, db, render_as_batch=True)
#     else:
#         migrate.init_app(app, db)
    

# da mettere in fondo per evitare gli import circolari
from blog import errors, models, routes