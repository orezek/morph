from app.models import Registration, Guests, UploadedFiles
from app.forms import RegCardForm
from flask import render_template, request, Blueprint
from app.helpers.data_model import website_metadata, navbar_metadata
from app.helpers.helpers import generate_session_id, save_uploaded_files_to_s3, convert_date, \
    radio_choice_mapper, create_guest_objects_from_form_data, create_uploaded_file_objects_from_form_data
from app import db

# for testing
import time

form_blueprint = Blueprint("form_blueprint", __name__, template_folder="templates/form")


@form_blueprint.route("/", methods=["GET", "POST"])
def form():
    reg_card_form = RegCardForm()
    if reg_card_form.validate_on_submit():
        start_time = time.perf_counter()
        request_id = generate_session_id(reg_card_form)
        save_uploaded_files_to_s3(request, request_id)
        registration_model = Registration(arrival=convert_date(reg_card_form.arrival.data),
                                          departure=convert_date(reg_card_form.departure.data),
                                          reservation_comment=reg_card_form.comment.data,
                                          reservation_source=radio_choice_mapper(int(reg_card_form.radio.data)),
                                          reg_id=request_id)
        db.session.add_all([registration_model])
        db.session.add_all(create_guest_objects_from_form_data(request_obj=request,
                                                               guest_model_obj=Guests,
                                                               no_guests=int(reg_card_form.no_guests.data),
                                                               reg_id=request_id))
        db.session.add_all(
            create_uploaded_file_objects_from_form_data(request_obj=request,
                                                        uploaded_files_model=UploadedFiles,
                                                        request_id=request_id))
        db.session.commit()
        reg_card_form = RegCardForm(formdata=None)
        end_time = time.perf_counter()
        print(end_time - start_time)
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
