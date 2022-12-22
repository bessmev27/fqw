import hashlib
import uuid
import datetime


def generate_user_root_key():
    return str(uuid.uuid4())


def generate_file_key(name: str):
    result = (name + str(datetime.datetime.now())).encode("utf-8")
    return hashlib.md5(result).hexdigest()
