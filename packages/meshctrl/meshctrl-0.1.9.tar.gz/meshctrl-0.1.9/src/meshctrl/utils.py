import time
import uuid
from base64 import b64encode

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes


def get_auth_token(user: str, key: str) -> str:
    key = bytes.fromhex(key)
    key1 = key[0:32]
    msg = '{{"userid":"{}", "domainid":"{}", "time":{}}}'.format(
        f"user//{user}", "", int(time.time())
    )
    iv = get_random_bytes(12)

    a = AES.new(key1, AES.MODE_GCM, iv)
    msg, tag = a.encrypt_and_digest(bytes(msg, "utf-8"))

    return b64encode(iv + tag + msg, altchars=b"@$").decode("utf-8")

def b64_to_hex(hex: str) -> str:
    return (
        b64encode(bytes.fromhex(hex)).decode().replace(r"/", "$").replace(r"+", "@")
    )

def gen_response_id() -> str:
    return str(uuid.uuid4())
