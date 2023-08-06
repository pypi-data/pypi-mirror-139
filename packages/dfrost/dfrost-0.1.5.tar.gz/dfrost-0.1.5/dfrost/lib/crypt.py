from dfrost.lib.log import debug
from cryptography.fernet import Fernet
from base64 import urlsafe_b64decode, urlsafe_b64encode


def get_chunk_size():
    return 64 * 1024 * 1024


def encrypt_file(src, dst):
    debug(f"Encrypting file: {src}, writing to: {dst}")
    with open(src, "rb") as src_f:
        with open(dst, "wb") as dst_f:
            key = Fernet.generate_key()
            dst_f.write(urlsafe_b64decode(key))
            while True:
                byte_data = src_f.read(get_chunk_size())
                if byte_data == b"":
                    break
                encrypted = urlsafe_b64decode(Fernet(key).encrypt(byte_data))
                dst_f.write(len(encrypted).to_bytes(4, "big"))
                dst_f.write(encrypted)


def decrypt_file(src, dst):
    debug(f"Decrypting file: {src}, writing to: {dst}")
    with open(src, "rb") as src_f:
        with open(dst, "wb") as dst_f:
            key = urlsafe_b64encode(src_f.read(32))
            while True:
                header = src_f.read(4)
                if header == b"":
                    break
                chunk_size = int.from_bytes(header, "big")
                byte_data = urlsafe_b64encode(src_f.read(chunk_size))
                dst_f.write(Fernet(key).decrypt(byte_data))
