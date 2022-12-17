import hashlib
import os
import random
import boto3
from botocore.exceptions import ClientError
from s3transfer import S3UploadFailedError
from werkzeug.utils import secure_filename
from datetime import datetime

BUCKET_NAME = "aurora-form-hotel"


# Generates a random unique session string. Is using SHA256
def generate_session_id(form_object) -> str:
    """
    Insert form object to get user data in order to generate a salt for the hash function
    :param form_object:
    :return: Hexadecimal unique string
    """
    utc_time = datetime.utcnow()
    ran_int = random.randint(0, 1000)
    salt0 = form_object.guest_name.data
    salt1 = form_object.guest_surname.data
    salt2 = form_object.email.data
    m = f"{ran_int}, {salt0}, {salt1}, {salt2}, {utc_time}"
    m = bytes(str(m), 'utf-8')
    hash_message = hashlib.sha256(m).hexdigest()
    return str(hash_message)[0:9]


# helper function to save files from the form
def save_uploaded_files(request_obj, application_obj) -> list:
    """
    saves files to a local directory and uses the filename from the user input
    :return: list of file names with absolute path
    """
    files = request_obj.files.getlist("files")
    links = []
    for file in files:
        f_name = os.path.join(application_obj.config["UPLOAD_FOLDER"], secure_filename(file.filename))
        file.save(f_name)
        links.append(f_name)
    return links


# save files to AWS S3
def upload_to_s3(file_name: str, bucket_name: str, object_name: str):
    s3 = boto3.client("s3")
    try:
        s3.upload_file(file_name, bucket_name, object_name)
    except ClientError as e:
        print(e)
    except S3UploadFailedError as e:
        print(e)


def save_uploaded_files_s3(request_obj, application_obj):
    """
    save files to a local directory and use the filename from the user input to initiate upload to s3 bucket in AWS
    :return: list of file names with absolute path
    """
    files = request_obj.files.getlist("files")
    links = []
    for file in files:
        f_name = os.path.join(application_obj.config["UPLOAD_FOLDER"], secure_filename(file.filename))
        file.save(f_name)
        links.append(f_name)
        upload_to_s3(f_name, BUCKET_NAME, secure_filename(file.filename))
    return links


def list_buckets() -> str:
    s3 = boto3.client("s3")
    buckets = s3.list_buckets()
    for bucket in buckets["Buckets"]:
        print(bucket["Name"])


def convert_date(form_date: datetime.date) -> datetime.date:
    """
    Converts date value from the forms fields to python date that DB can well understand.
    :param form_date: date from the HTML form
    :return: date in Python date time format
    """
    date = datetime.strptime(str(form_date), "%Y-%m-%d")
    return date


def radio_choice_mapper(form_field: int) -> str:
    """
    Convert an integer value to string of choice
    :param form_field: int value from the form radio field
    :return: string representation of the value from the form field
    """
    choices = {
        1: "Friend or family member",
        2: "Travel agency or similar",
        3: "Internet search",
        4: "Magazine or similar",
        5: "Design Hotels",
        6: "Design Hotels",
        7: "Other"
    }
    return choices.get(form_field, "Invalid value")


def title_selection_mapper(form_title_field: str) -> str:
    """
    Mapper that converts choice string selection into more human-readable form
    :param form_title_field:
    :return: string with correct title form
    """
    title = {
        "mr": "Mr",
        "mrs": "Mrs",
        "ms": "Ms",
        "mas": "Master",
        "miss": "Miss"
    }
    return title.get(form_title_field, "No value chosen")

if __name__ == "__main__":
     # list_buckets()
    print(len("/Users/aldokezer/Development/morphe/app/static/uploaded_files/Monika_passport.jpeg"))

