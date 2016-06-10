from string import punctuation
from os import urandom
from base64 import b64encode


def generate_password(count=8, _bytes=False, _printable=False):
    """Function for generate passwords.
    Create password from os.urandom(count) in bytes and return in needed view.

    :param int count: length of password what should return
    :param bool _bytes: flag for return password in bytes
    :param bool _printable: flag for return password only with printable
                characters

    """
    if _bytes:
        return urandom(count)

    password = urandom(count + 5)
    encrypt_b64 = b64encode(password).decode('utf-8')
    if _printable:
        psw = [_chr for _chr in encrypt_b64 if _chr not in punctuation]
        return ''.join(psw[:count])
    else:
        return encrypt_b64[:count]
