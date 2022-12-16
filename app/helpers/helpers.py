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
    ran_int = random.randint(0, 1000)
    salt0 = form_object.guest_name.data
    salt1 = form_object.guest_surname.data
    salt2 = form_object.email.data
    m = f"{ran_int}, {salt0}, {salt1}, {salt2}"
    m = bytes(str(m), 'utf-8')
    hash_message = hashlib.sha256(m).hexdigest()
    return str(hash_message)[0:10]


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


def radio_choice_convertor(form_field) -> str:
    """
    Converts int value returned from HTML form into the actual choice option
    :param form_field: data from the HTML field
    :return: String choice value provided in the HTML form
    """
    if form_field == "1":
        return "Friend or family member"
    elif form_field == "2":
        return "Travel agency or similar"
    elif form_field == "3":
        return "Internet search"
    elif form_field == "4":
        return "Magazine or similar"
    elif form_field == "5":
        return "Design Hotels"
    elif form_field == "6":
        return "Design Hotels"
    elif form_field == "7":
        return "Other"
    else:
        return "No value selected"


# if __name__ == "__main__":
#     # list_buckets()
