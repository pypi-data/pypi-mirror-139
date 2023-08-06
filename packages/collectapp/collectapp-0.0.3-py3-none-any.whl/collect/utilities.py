import json
import random
import string
import hmac
import base64
import hashlib
import time
import requests

base_url = 'https://sandboxapi.rapyd.net'

access_key = 'A4FBE640774F867A1155'
secret_key = ('0083afb478abde4bbc0b64c2b706ca85fd93e' +
              'fac4b0ac65af53f70622b89559f4e0bcd79705b3ff3')


def generate_salt(length=12):
    return ''.join(random.sample(string.ascii_letters + string.digits, length))


def get_unix_time(days=0, hours=0, minutes=0, seconds=0):
    return int(time.time())


def update_timestamp_salt_sig(http_method, path, body):
    if path.startswith('http'):
        path = path[path.find('/v1'):]
    salt = generate_salt()
    timestamp = get_unix_time()
    to_sign = (
        http_method, path, salt, str(timestamp), access_key, secret_key, body)

    h = hmac.new(
        secret_key.encode('utf-8'),
        ''.join(to_sign).encode('utf-8'), hashlib.sha256)
    signature = base64.urlsafe_b64encode(str.encode(h.hexdigest()))
    return salt, timestamp, signature


def current_sig_headers(salt, timestamp, signature):
    sig_headers = {'access_key': access_key,
                   'salt': salt,
                   'timestamp': str(timestamp),
                   'signature': signature,
                   'idempotency': str(get_unix_time()) + salt}
    return sig_headers


def pre_call(http_method, path, body=None):
    str_body = json.dumps(
        body, separators=(',', ':'), ensure_ascii=False) if body else ''
    salt, timestamp, signature = update_timestamp_salt_sig(
        http_method=http_method, path=path, body=str_body)
    return str_body.encode('utf-8'), salt, timestamp, signature


def create_headers(http_method, url, body=None):
    body, salt, timestamp, signature = pre_call(
        http_method=http_method, path=url, body=body)
    return body, current_sig_headers(salt, timestamp, signature)


def make_request(method, path, body=''):
    body, headers = create_headers(method, base_url + path, body)

    if method == 'get':
        response = requests.get(base_url + path, headers=headers)
    elif method == 'put':
        response = requests.put(base_url + path, data=body, headers=headers)
    elif method == 'delete':
        response = requests.delete(base_url + path, data=body, headers=headers)
    else:
        response = requests.post(base_url + path, data=body, headers=headers)

    if response.status_code != 200:
        raise TypeError(response.content, method, base_url + path)
    return json.loads(response.content)


def test_request(method, path, body=''):
    body, headers = create_headers(method, base_url + path, body)

    if method == 'get':
        response = requests.get(base_url + path, headers=headers)
    elif method == 'put':
        response = requests.put(base_url + path, data=body, headers=headers)
    elif method == 'delete':
        response = requests.delete(base_url + path, data=body, headers=headers)
    else:
        response = requests.post(base_url + path, data=body, headers=headers)

    return response
