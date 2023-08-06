import hashlib

import os
import base64


def generate_sha256_string(input_string):
    m = hashlib.sha256()
    m.update(input_string.encode('utf-8'))
    return m.hexdigest()


def generate_os_urandom_string(size):
    random_bytes = os.urandom(size)
    token = base64.urlsafe_b64encode(random_bytes).decode('utf-8')
    return token
