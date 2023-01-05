from app.models import Registration, Guests, UploadedFiles
from app.forms import RegCardForm
from flask import render_template, request, Blueprint
from app.helpers.data_model import website_metadata, navbar_metadata
from app.helpers.helpers import generate_session_id, save_uploaded_files_to_s3, convert_date, \
    radio_choice_mapper, title_selection_mapper, create_guest_objects_from_form_data
from app import db

# for testing
import time

form_blueprint = Blueprint("form_blueprint", __name__, template_folder="templates/form")


@form_blueprint.route("/", methods=["GET", "POST"])
def form():
    reg_card_form = RegCardForm()
    if reg_card_form.validate_on_submit():
        start_time = time.time()
        reg_id = generate_session_id(reg_card_form)
        links = save_uploaded_files_to_s3(request, reg_id)  # save uploaded files to S3 and return links
        reg = Registration(convert_date(reg_card_form.arrival.data),
                           convert_date(reg_card_form.departure.data),
                           reg_card_form.comment.data,
                           radio_choice_mapper(int(reg_card_form.radio.data)),
                           reg_id)
        uploaded_file_objects = []
        for link in links:
            uploaded_file_objects.append(UploadedFiles(link, is_signature=False, reg_id=reg_id))
        db.session.add_all([reg])
        db.session.add_all(
            create_guest_objects_from_form_data(request, Guests, int(reg_card_form.no_guests.data), reg_id=reg_id))
        db.session.add_all(uploaded_file_objects)
        db.session.commit()
        reg_card_form = RegCardForm(formdata=None)
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(elapsed_time)
        return render_template("form.html",
                               website_metadata=website_metadata,
                               navbar_metadata=navbar_metadata,
                               reg_card_form=reg_card_form
                               )
    return render_template("form.html",
                           website_metadata=website_metadata,
                           navbar_metadata=navbar_metadata,
                           reg_card_form=reg_card_form
                           )
