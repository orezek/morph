import hashlib
import os
import random
import boto3
import flask
from botocore.exceptions import ClientError
from s3transfer import S3UploadFailedError
from werkzeug.utils import secure_filename
from datetime import datetime

BUCKET_NAME = "aurora-form-hotel"
BUCKET_URL = f"https://{BUCKET_NAME}.s3.eu-central-1.amazonaws.com/"


# Generates a random unique session string. Is using SHA256
def generate_session_id(form_object) -> str:
    """
    Function that generates a random string of length 10 chars for identifying each post request.
    :param form_object: form object for using data from the form to generate the hash
    :return: Hexadecimal unique string
    """
    utc_time = datetime.utcnow()
    ran_int = random.randint(0, 1000)
    salt0 = form_object.guest_name1.data
    salt1 = form_object.guest_surname1.data
    salt2 = form_object.email1.data
    m = f"{ran_int}, {salt0}, {salt1}, {salt2}, {utc_time}"
    m = bytes(str(m), 'utf-8')
    hash_message = hashlib.sha256(m).hexdigest()
    return str(hash_message)[0:9]


# helper function to save files from the form
def save_uploaded_files(request_obj: flask.Request, application_obj: flask) -> list:
    """
    Saves the files to a local directory and uses the filename from the user input.
    :param request_obj: Flask request object that holds form file data.
    :param application_obj: Flask application object as
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
def upload_to_s3(file_obj, bucket_name: str, object_name: str, file_content_type: str):
    """
    Saves data to S3 bucket in AWS
    :param file_obj: byte stream file object
    :param bucket_name: name of the AWS S3 bucket
    :param object_name: name of the file
    :param file_content_type: content type of the file
    :return: None
    """
    # FIXME: Change AWS authentication credentials.
    s3 = boto3.client("s3")
    try:
        s3.upload_fileobj(file_obj, bucket_name, object_name, ExtraArgs={'ContentType': file_content_type})
    except ClientError as e:
        print(e)
    except S3UploadFailedError as e:
        print(e)


def save_uploaded_files_to_s3(request_obj: flask.Request, prefix: str) -> list:
    """
    save files to a S3
    :param request_obj Flask reqeust object
    :param prefix Unique request or session id used for generating prefixes for S3 to group files.
    :return: list of file names with absolute path to S3 bucket
    """
    files = request_obj.files.getlist("files")
    for file in files:
        secured_file_name = secure_filename(file.filename)
        file_content_type = str(file.content_type)
        key = prefix + "/" + secured_file_name
        upload_to_s3(file, BUCKET_NAME, key, file_content_type)


def generate_s3_file_links(request_obj: flask.Request, prefix: str) -> list:
    """
    Generates html link for each uploaded file to S3
    :param request_obj: Flask request object
    :param prefix: unique string to group files by common identifier
    :return: list of links
    """
    files = request_obj.files.getlist("files")
    links = list()
    for file in files:
        secured_file_name = secure_filename(file.filename)
        file_link = BUCKET_URL + prefix + "/" + secured_file_name
        links.append(file_link)
    return links


def create_uploaded_file_objects_from_form_data(request_obj, uploaded_files_model, request_id) -> list:
    """
    Creates list of uploaded_file instances and adds them into a list
    :param request_obj: Flask request object
    :param uploaded_files_model: class for DB model UploadedFiles
    :param request_id: unique string for representing each request
    :return: list of instances of UploadedFiles class
    """
    uploaded_files_model_object_list = []
    for link in generate_s3_file_links(request_obj=request_obj, prefix=request_id):
        uploaded_files_model_object_list.append(uploaded_files_model(link, is_signature=False, reg_id=request_id))
    return uploaded_files_model_object_list


def list_buckets():
    """
    Prints list of buckets from my AWS account
    :return:
    """
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
    Mapper that converts choice string selection into more human-readable form.
    :param form_title_field: Form data from title field.
    :return: String with well-formed title.
    """
    title = {
        "mr": "Mr",
        "mrs": "Mrs",
        "ms": "Ms",
        "mas": "Master",
        "miss": "Miss"
    }
    return title.get(form_title_field, "No value chosen")


def create_guest_objects_from_form_data(request_obj, guest_model_obj, no_guests, reg_id) -> list:
    """
        Create a list of `guest_model_obj` instances from form data in a request object.
    :param request_obj: An object representing a request, from which form data will be extracted.
    :param guest_model_obj: A class representing a guest object.
    :param no_guests: The number of guests for which data is included in the form.
    :param reg_id: A unique session ID generated for each session.
    :return:
        list: A list of `guest_model_obj` instances created from the form data.
    """
    guests_to_save = []
    for number in range(1, no_guests + 1):
        is_leading_guest = True if number == 1 else False
        guests_to_save.append(guest_model_obj(
            is_leading_guest,
            title_selection_mapper(request_obj.form[f"title{number}"]),
            request_obj.form[f"guest_name{number}"],
            request_obj.form[f"guest_surname{number}"],
            request_obj.form[f"email{number}"],
            request_obj.form[f"tel{number}"],
            reg_id
        ))
    return guests_to_save


