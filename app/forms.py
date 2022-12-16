from flask_wtf import FlaskForm
from wtforms import (StringField, SubmitField, SelectField,
                     EmailField, TelField, DateField,
                     TextAreaField, MultipleFileField, RadioField, Label)

radio_choices = [(1, "Friend or family member"), (2, "Travel agency or similar"), (3, "Internet search"),
                 (4, "Magazine or similar"), (5, "Social media or similar"), (6, "Design Hotels"),
                 (7, "Other")]


class RegCardForm(FlaskForm):
    no_guests = SelectField("Number of Guests", choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7)])
    title = SelectField("Title",
                        choices=[("mr", "Mr"), ("mrs", "Mrs"), ("ms", "Ms"), ("mas", "Master"), ("miss", "Miss")])
    guest_name = StringField("Guest Name")
    guest_surname = StringField()
    email = EmailField("Email")
    tel = TelField("Phone Number")
    arrival = DateField("Arrival")
    departure = DateField("Departure")
    comment = TextAreaField("Any additional information that you would like to share with us? (allergies, "
                            "anniversary, honeymoon, birthday…)")
    files = MultipleFileField("Upload passport photo of all travelers")
    radio = RadioField("",
                       choices=radio_choices)
    # signature field = to do!
    submit = SubmitField("Submit")
