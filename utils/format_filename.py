import os
from uuid import uuid4


def format_filename(file):
    filename, ext = os.path.splitext(file.filename)
    filename = str(uuid4())
    return filename + ext
