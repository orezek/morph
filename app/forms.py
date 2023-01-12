from flask_wtf import FlaskForm
from wtforms import (StringField, SubmitField, SelectField,
                     EmailField, TelField, DateField,
                     TextAreaField, MultipleFileField, RadioField, Label)

from wtforms.validators import DataRequired

# select options for radio field
radio_choices = [(1, "Friend or family member"), (2, "Travel agency or similar"), (3, "Internet search"),
                 (4, "Magazine or similar"), (5, "Social media or similar"), (6, "Design Hotels"),
                 (7, "Other")]

# select options for no_guests field
no_guests_choice = [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7)]

# select options for title field
title_choices = [("mr", "Mr"), ("mrs", "Mrs"), ("ms", "Ms"), ("mas", "Master"), ("miss", "Miss")]

# regex pattern for email validation
email_pattern = "^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$"

# text area label
text_area_label_text = "Any additional information that you would like to share with us? (allergies,anniversary, " \
                       "honeymoon, birthday…)"

# upload file field text label
upload_file_field_label = "Upload passport photo of all travelers"

# tell field additional kw parameters to for better styling of the field
tel_kw = {"placeholder": "Enter your phone number", "pattern": "^\+?[0-9\s]*$", "minlength": "12", "maxlength": "20"}

# email field additional kw parameters to for better styling of the field
email_kw = {"placeholder": "Enter your email", "pattern": email_pattern}

guest_name_kw = {"placeholder": "First name"}

surname_kw = {"placeholder": "Last name"}

radio_kw = {"class": "form-check-input"}


# TODO set file upload size limit
class RegCardForm(FlaskForm):
    no_guests = SelectField("Number of Guests", choices=no_guests_choice)
    title1 = SelectField("Title", choices=title_choices)
    guest_name1 = StringField("Guest Name", validators=[DataRequired()], render_kw=guest_name_kw)
    guest_surname1 = StringField("", validators=[DataRequired()], render_kw=surname_kw)
    email1 = EmailField("Email", validators=[DataRequired()], render_kw=email_kw)
    tel1 = TelField("Phone Number", validators=[DataRequired()], render_kw=tel_kw)
    arrival = DateField("Arrival", validators=[DataRequired()])
    departure = DateField("Departure", validators=[DataRequired()])
    comment = TextAreaField(text_area_label_text)
    files = MultipleFileField(upload_file_field_label, validators=[DataRequired()])
    radio = RadioField("", choices=radio_choices, validators=[DataRequired()], render_kw=radio_kw)
    # TODO Signature field from canvas.
    submit = SubmitField("Submit")
