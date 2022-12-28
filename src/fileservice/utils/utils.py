import hashlib
import uuid
from datetime import datetime


def generate_refresh_token():
    return str(uuid.uuid4())


def generate_file_key(name: str):
    result = (name + str(datetime.now())).encode("utf-8")
    return hashlib.md5(result).hexdigest()
