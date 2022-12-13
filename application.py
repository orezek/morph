import os
import random

from flask import Flask, render_template, request
from flask_migrate import Migrate
from werkzeug.utils import secure_filename

from data_model import website_metadata, navbar_metadata
from forms import RegCardForm
from models import Registration, Guests, UploadedFiles, db
import hashlib

# define root project and upload location
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(APP_ROOT, "static", "uploaded_files")

# DB engine and connection setup - make ENV or AWS Param. store
user_name = "admin"
password = "Mirodinga1"
db_engine_driver = "mysql+pymysql"
db_url = "aurora-app-prod.ccj4auatnl5l.eu-central-1.rds.amazonaws.com"
db_port = "3306"
db_name = "aurora"
db_charset = "charset=utf8mb4"
# SQLite DB connection for local testing
db_connection_sqlite = "sqlite:///" + os.path.join(APP_ROOT, "data.sqlite")
# MariaDB's connection for AWS RDS database
db_connection_mariadb = f"{db_engine_driver}://{user_name}:{password}@{db_url}:{db_port}/{db_name}?{db_charset}"

application = Flask(__name__)
# hide or make it ENV or save to AWS to parameter store
application.config["SECRET_KEY"] = "some_secret"
application.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
application.config["SQLALCHEMY_DATABASE_URI"] = db_connection_sqlite

# initiate DB
db.init_app(application)
Migrate(application, db, render_as_batch=True)

# TO DO
# form add features 1) canvas for signatures 2) dynamic fields for multiple guests
# add field validation
# make secret key random string and environmental variable or use secrets or ssm parameter store in AWS


# helper function to save files from the form
def save_uploaded_files() -> list:
    """
    saves files to a local directory and uses the filename from the user input
    :return: list of file names with absolute path
    """
    files = request.files.getlist("files")
    links = []
    for file in files:
        f_name = os.path.join(application.config["UPLOAD_FOLDER"], secure_filename(file.filename))
        file.save(f_name)
        links.append(f_name)
    return links


# Generates a random unique session string. Is using SHA256
def generate_session_id(form_object: RegCardForm) -> str:
    """
    Insert form object to get user data in order to generate a salt for the hash function
    :param form_object:
    :return: Hexadecimal unique string
    """
    ran_int = random.randint(0, 1000)
    salt0 = form_object.guest_name.data
    salt1 = form_object.guest_surname.data
    salt2 = form_object.email.data
    m = f"{ran_int}, {salt0}, {salt1}, {salt2}"
    m = bytes(str(m), 'utf-8')
    hash_message = hashlib.sha256(m).hexdigest()
    return str(hash_message)[0:10]


@application.route("/", methods=["GET", "POST"])
def form():
    reg_card_form = RegCardForm()
    if reg_card_form.validate_on_submit():
        reg_id = generate_session_id(reg_card_form)
        links = save_uploaded_files()
        # test the db on some data from the actual form, the rest is hardcoded
        reg = Registration(reg_card_form.arrival.data,
                           reg_card_form.departure.data,
                           reg_card_form.comment.data,
                           reg_card_form.radio.data,
                           reg_id)
        guest = Guests("False",
                       reg_card_form.title.data,
                       reg_card_form.guest_name.data,
                       reg_card_form.guest_surname.data,
                       reg_card_form.email.data,
                       reg_card_form.tel.data,
                       reg_id)
        for link in links:
            files = UploadedFiles(link, "False", reg_id)
            db.session.add(files)
            db.session.commit()
        db.session.add_all([reg, guest])
        db.session.commit()
        # end of DB code
        reg_card_form = RegCardForm(formdata=None)
        return render_template("form.html", website_metadata=website_metadata,
                               navbar_metadata=navbar_metadata,
                               reg_card_form=reg_card_form)
    return render_template("form.html", website_metadata=website_metadata,
                           navbar_metadata=navbar_metadata,
                           reg_card_form=reg_card_form)


if __name__ == "__main__":
    application.run(debug=True, port=5001)
