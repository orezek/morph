from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_debugtoolbar import DebugToolbarExtension
from config import Config
from dotenv import load_dotenv

# Load env variables from .env file
load_dotenv()

# Set models
db = SQLAlchemy()

application = Flask(__name__)
application.config.from_object(Config)

# initiate DB
db.init_app(application)
Migrate(application, db, render_as_batch=True)

from app.views import form_blueprint
application.register_blueprint(form_blueprint, url_prefix="/")

# Debug Toolbar
#toolbar = DebugToolbarExtension(application)
