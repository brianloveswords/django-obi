import os
import base64
import hashlib
import json

from django.utils.encoding import smart_str


def base64url_decode(input):
    input += '=' * (4 - (len(input) % 4))
    return base64.urlsafe_b64decode(input)


def base64url_encode(input):
    return base64.urlsafe_b64encode(input).replace('=', '')


def encode_badge(badge_id, username):
    raw_json = json.dumps({'username': username, 'id': badge_id})
    return base64url_encode(raw_json)


def decode_badge(identifier):
    try:
        data = json.loads(base64url_decode(identifier))
        return data['id'], data['username']
    except (UnicodeEncodeError, ValueError, KeyError):
        return None


def get_hexdigest(algorithm, salt, raw_email):
    """Generate email hash."""
    return hashlib.new(algorithm, smart_str(raw_email + salt)).hexdigest()


def hash_recipient(raw_email, algorithm='sha256'):
    """Create salted, hashed receipient."""
    salt = os.urandom(5).encode('hex')
    hsh = get_hexdigest(algorithm, salt, raw_email)
    return '$'.join((algorithm, hsh)), salt
