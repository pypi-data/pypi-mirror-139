from dfrost.lib.log import debug
from itertools import count
from random import randint


def get_chunk_size():
    return 64 * 1024


def mangle_file(src, dst):
    debug(f"Mangling file: {src}, writing to: {dst}")
    with open(src, "rb") as src_f:
        with open(dst, "wb") as dst_f:
            last_byte = randint(0, 255)
            dst_f.write(bytes([last_byte]))
            for ix in count():
                byte_data = bytearray(src_f.read(get_chunk_size()))
                if byte_data == b"":
                    break
                for ix in range(len(byte_data)):
                    byte_data[ix] ^= last_byte
                    last_byte = byte_data[ix]
                dst_f.write(byte_data)


def unmangle_file(src, dst):
    debug(f"Unmangling file: {src}, writing to: {dst}")
    with open(src, "rb") as src_f:
        with open(dst, "wb") as dst_f:
            last_byte = src_f.read(1)[0]
            for ix in count():
                byte_data = bytearray(src_f.read(get_chunk_size()))
                if byte_data == b"":
                    break
                for ix in range(len(byte_data)):
                    obfuscated_byte = byte_data[ix]
                    byte_data[ix] ^= last_byte
                    last_byte = obfuscated_byte
                dst_f.write(byte_data)
