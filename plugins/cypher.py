"""
cypher.py

Ciphers and deciphers strings.

Created By:
    - Tom <https://github.com/instanceoftom>

Modified By:
    - Fletcher Boyd <https://github.com/thenoodle68>
    - Dabo Ross <https://github.com/daboross>
    - Luke Rogers <https://github.com/lukeroge>

License:
    GPL v3
"""

import base64
import binascii

from cloudbot import hook


def encode(password, text):
    """
    :type password: str
    :type text: str
    """
    enc = []
    for i, c in enumerate(text):
        key_c = password[i % len(password)]
        enc_c = chr((ord(c) + ord(key_c)) % 256)
        enc.append(enc_c)
    return base64.urlsafe_b64encode("".join(enc).encode()).decode()


def decode(password, encoded, notice):
    """
    :type password: str
    :type encoded: str
    """
    dec = []
    try:
        encoded_bytes = base64.urlsafe_b64decode(encoded.encode()).decode()
    except binascii.Error:
        notice("Invalid input '{}'".format(encoded))
        return
    for i, c in enumerate(encoded_bytes):
        key_c = password[i % len(password)]
        dec_c = chr((256 + ord(c) - ord(key_c)) % 256)
        dec.append(dec_c)
    return "".join(dec)


@hook.command("cypher", "cipher")
def cypher(text, message, event):
    """<pass> <string> - cyphers <string> with <password>"""
    split = text.split(None, 1)
    if len(split) < 2:
        event.notice_doc()
        return
    password = split[0]
    plaintext = split[1]
    message(" " + encode(password, plaintext))


@hook.command("decypher", "decipher")
def decypher(text, message, notice, event):
    """<pass> <string> - decyphers <string> with <password>"""
    split = text.split(None, 1)
    if len(split) < 2:
        event.notice_doc()
        return
    password = split[0]
    encoded = split[1]
    message(" " + decode(password, encoded, notice))
