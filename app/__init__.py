from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from app.utils import check_roles

app = Flask(__name__)
app.config.from_object(Config)
app.jinja_env.globals['check_roles'] = check_roles
login = LoginManager(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
from app import routes, models
