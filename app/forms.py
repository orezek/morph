from flask_wtf import FlaskForm
from wtforms import (StringField, SubmitField, SelectField,
                     EmailField, TelField, DateField,
                     TextAreaField, MultipleFileField, RadioField, Label)

from wtforms.validators import DataRequired

radio_choices = [(1, "Friend or family member"), (2, "Travel agency or similar"), (3, "Internet search"),
                 (4, "Magazine or similar"), (5, "Social media or similar"), (6, "Design Hotels"),
                 (7, "Other")]

# regex pattern for email validation
email_pattern = "^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$"


# TODO set file upload size limit
class RegCardForm(FlaskForm):
    no_guests = SelectField("Number of Guests", choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7)])
    title1 = SelectField("Title",
                        choices=[("mr", "Mr"), ("mrs", "Mrs"), ("ms", "Ms"), ("mas", "Master"), ("miss", "Miss")])
    guest_name1 = StringField("Guest Name", validators=[DataRequired()], render_kw={"placeholder": "First name"})
    guest_surname1 = StringField("", validators=[DataRequired()], render_kw={"placeholder": "Last name"})
    email1 = EmailField("Email", validators=[DataRequired()],
                       render_kw={"placeholder": "Enter your email", "pattern": email_pattern})
    tel1 = TelField("Phone Number", validators=[DataRequired()],
                   render_kw={"placeholder": "Enter your phone number",
                              "pattern": "^\+?[0-9\s]*$", "minlength": "12", "maxlength": "20"})
    arrival = DateField("Arrival", validators=[DataRequired()])
    departure = DateField("Departure", validators=[DataRequired()])
    comment = TextAreaField("Any additional information that you would like to share with us? (allergies, "
                            "anniversary, honeymoon, birthday…)")
    files = MultipleFileField("Upload passport photo of all travelers", validators=[DataRequired()])
    radio = RadioField("", choices=radio_choices, validators=[DataRequired()], render_kw={"class": "form-check-input"})
    # signature field = to do!
    submit = SubmitField("Submit")
