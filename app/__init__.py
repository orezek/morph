from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from config import Config

# Set models
db = SQLAlchemy()

application = Flask(__name__)
application.config.from_object(Config)

# initiate DB
db.init_app(application)
Migrate(application, db, render_as_batch=True)

from app.views import form_blueprint
application.register_blueprint(form_blueprint, url_prefix="/")
