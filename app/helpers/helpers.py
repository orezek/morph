import hashlib
import os
import random

from werkzeug.utils import secure_filename


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


