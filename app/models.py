from datetime import datetime
from app import db


class Registration(db.Model):
    """
    Registration table
    """
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    reg_id = db.Column(db.String(10), unique=True)
    reservation_no = db.Column(db.String(20), default=None)
    arrival = db.Column(db.Date)
    departure = db.Column(db.Date)
    reservation_comment = db.Column(db.String(1000))
    reservation_source = db.Column(db.String(50))
    guest = db.relationship("Guests", backref="registration", lazy="dynamic")
    file = db.relationship("UploadedFiles", backref="registration", lazy="dynamic")

    def __init__(self, arrival, departure, reservation_comment, reservation_source, reg_id):
        """
        Constructor for registration object
        :param arrival:
        :param departure:
        :param reservation_comment:
        :param reservation_source:
        :param reg_id:
        """
        self.arrival = arrival
        self.departure = departure
        self.reservation_comment = reservation_comment
        self.reservation_source = reservation_source
        self.reg_id = reg_id

    def __repr__(self):
        return f"{self.reg_id}, {self.arrival}, {self.departure}," \
               f"{self.reservation_comment}, {self.reservation_source}," \
               f"{self.guest.guest_name}"


class Guests(db.Model):
    """
    Guest table
    """
    id = db.Column(db.Integer, primary_key=True)
    reg_id = db.Column(db.String(10), db.ForeignKey("registration.reg_id", ondelete="CASCADE", onupdate="CASCADE"))
    leading_guest = db.Column(db.Boolean, default=False)
    title = db.Column(db.String(10))
    guest_name = db.Column(db.String(100))
    guest_surname = db.Column(db.String(100))
    guest_email = db.Column(db.String(100))
    guest_phone = db.Column(db.String(50))

    def __init__(self, leading_guest, title, guest_name, guest_surname, guest_email, guest_phone, reg_id):
        self.leading_guest = leading_guest
        self.title = title
        self.guest_name = guest_name
        self.guest_surname = guest_surname
        self.guest_email = guest_email
        self.guest_phone = guest_phone
        self.reg_id = reg_id

    def __repr__(self):
        return f"{self.leading_guest}, {self.title}, {self.guest_name}," \
               f"{self.guest_surname}, {self.guest_email}, {self.guest_phone}, {self.reg_id}"


class UploadedFiles(db.Model):
    """
    Uploaded files table for data uploaded from the form.
    """
    id = db.Column(db.Integer, primary_key=True)
    reg_id = db.Column(db.String(10), db.ForeignKey("registration.reg_id", ondelete="CASCADE", onupdate="CASCADE"))
    file_link = db.Column(db.String(500))
    is_signature = db.Column(db.Boolean, default=False)

    def __init__(self, file_link, is_signature, reg_id):
        """
        Creates table object UploadedFiles in SQL database
        :param file_link: string link to a file object
        :param is_signature: boolean value indication whether the file object is signature
        :param reg_id: unique string for give session
        """
        self.file_link = file_link
        self.is_signature = is_signature
        self.reg_id = reg_id

    def __repr__(self):
        return f"{self.id}, {self.reg_id}, {self.file_link}, {self.is_signature}"






