from app.models import Registration, Guests, UploadedFiles
from app.forms import RegCardForm
from app import application
from flask import render_template, request, Blueprint
from app.helpers.data_model import website_metadata, navbar_metadata
from app.helpers.helpers import generate_session_id, save_uploaded_files_s3, convert_date, \
    radio_choice_mapper, title_selection_mapper
from app import db


form_blueprint = Blueprint("form_blueprint", __name__, template_folder="templates/form")


@form_blueprint.route("/", methods=["GET", "POST"])
def form():
    reg_card_form = RegCardForm()
    if reg_card_form.validate_on_submit():
        reg_id = generate_session_id(reg_card_form)
        links = save_uploaded_files_s3(request, application)
        reg = Registration(convert_date(reg_card_form.arrival.data),
                           convert_date(reg_card_form.departure.data),
                           reg_card_form.comment.data,
                           radio_choice_mapper(int(reg_card_form.radio.data)),
                           reg_id)
        guest = Guests(False,
                       title_selection_mapper(reg_card_form.title.data),
                       reg_card_form.guest_name.data,
                       reg_card_form.guest_surname.data,
                       reg_card_form.email.data,
                       reg_card_form.tel.data,
                       reg_id)
        db.session.add_all([reg, guest])
        db.session.commit()
        for link in links:
            files = UploadedFiles(link, False, reg_id)
            db.session.add(files)
            db.session.commit()
        # end of DB code
        reg_card_form = RegCardForm(formdata=None)
        return render_template("form.html", website_metadata=website_metadata,
                               navbar_metadata=navbar_metadata,
                               reg_card_form=reg_card_form)
    return render_template("form.html", website_metadata=website_metadata,
                           navbar_metadata=navbar_metadata,
                           reg_card_form=reg_card_form)
