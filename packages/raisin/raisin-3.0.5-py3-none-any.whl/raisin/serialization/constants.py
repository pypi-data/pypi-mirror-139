#!/usr/bin/env python3

"""
** All major constants and invariants for serialization. **
-----------------------------------------------------------
"""

BUFFER_SIZE = 8 * 1024 * 1024  # packet size in bytes
ALPHABET = [
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's',
    't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
    'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '0', '1', '2', '3', '4',
    '5', '6', '7', '8', '9', '!', '#', '$', '_', '&', '(', ')', '*', '+', ']', '-', '.', '/', ':',
    ';', '<', '=', '>', '?', '@', '[']  # alphabet to convert bytes in ascii str
N_SYMB = 64  # nbr of ascii char to encode *N_BYTES* : 51*log(256)/log(len(ALPHABET)) = 63.9996
N_BYTES = 51  # number of bytes to group before converting them into ascii str
HEADER = {
    'header': [b'/header/', b'\x00'],
    # 'json': [b'/json/', b'\x01'],
    'dumps': [b'0', b'\x30'], # b'\x48' == b'0'
    'small_int': [b'/small int/', b'\x02'],
    'large_int': [b'/large int/', b'\x03'],
    # 'filename': [b'/filename + file_content/', b'\x04'],
    'str': [b'/str/', b'\x05'],
    'round_float': [b'/round float/', b'\x06'],
    'normal_float': [b'/normal float/', b'\x07'],
    'float': [b'/float/', b'\x08'],
    'bytes': [b'/bytes/', b'\x09'],
    # 'TextIOWrapper': [b'/io.TextIOWrapper/', b'\x0a'],
    # 'BufferedReader': [b'/io.BufferedReader/', b'\x0b'],
    # 'BufferedWriter': [b'/io.BufferedWriter/', b'\x0c'],
    'list': [b'/list/', b'\x0d'],
    'tuple': [b'/tuple/', b'\x0e'],
    # 'dict': [b'/dict/', b'\x0f'],
    # 'complex': [b'/complex/', b'\x10'],
    # 'class': [b'/class/', b'\x11'],
    # 'callable': [b'/callable/', b'\x12'],
    'null': [b'/none/', b'\x13'],
    'true': [b'/true/', b'\x14'],
    'false': [b'/false/', b'\x15'],
    # 'set': [b'/set/', b'\x16'],
    # 'frozenset': [b'/frozenset/', b'\x17'],
    'generator': [b'/generator/', b'\x18'],
    'function': [b'/function/', b'\x19'],
    # 'rsa_bloc': [b'/rsa bloc/', b'\x20'],
    # 'aes_gen': [b'/aes gen/', b'\x21'],
    # 'rsa_gen': [b'/rsa gen/', b'\x22'],
    # 'aes_sel': [b'/aes sel/', b'\x23'],
    # 'authenticity': [b'/authenticity/', b'\x24'],
    'argument': [b'/argument/', b'\x25'],
    'func': [b'/func/', b'\x26'],
    'task': [b'/task/', b'\x27'],
    'result': [b'/result/', b'\x28'],
    'identity': [b'/identity/', b'\x29'],
}  # serialized data headers, (forbiden b'\x2f' = b'/')

ALPHABET2INDEX = {s: i for i, s in enumerate(ALPHABET)}  # to each ascii char, associates its index
BYTES2HEADER = {
    bytes_header: str_header
    for str_header, bytes_headers in HEADER.items()
    for bytes_header in bytes_headers
}  # to each bytes header, associates its name str
HEADERLEN = {
    size: any(h for h in BYTES2HEADER if len(h) > size)
    for size in range(max(len(h) for h in BYTES2HEADER) + 1)
}  # at each size, gives True if exists a bytes header of len > size
