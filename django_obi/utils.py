import base64
import json


def base64url_decode(input):
    input += '=' * (4 - (len(input) % 4))
    return base64.urlsafe_b64decode(input)


def base64url_encode(input):
    return base64.urlsafe_b64encode(input).replace('=', '')


def encode_badge(badge_id, email):
    raw_json = json.dumps({'email': email, 'id': badge_id})
    return base64url_encode(raw_json)


def decode_badge(identifier):
    try:
        data = json.loads(base64url_decode(identifier))
        return data['id'], data['email']
    except (UnicodeEncodeError, ValueError, KeyError):
        return None
