import binascii
import struct

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import (Cipher, aead, algorithms,
                                                    modes)
from cryptography.hazmat.primitives.kdf.hkdf import HKDF, HKDFExpand

from .packet import is_long_header

algorithm = hashes.SHA256()
backend = default_backend()

INITIAL_SALT = binascii.unhexlify('ef4fb0abb47470c41befcf8031334fae485e09a0')


def hkdf_label(label, length):
    full_label = b'tls13 ' + label
    return struct.pack('!HB', length, len(full_label)) + full_label + b'\x00'


def hkdf_expand_label(secret, label, length):
    return HKDFExpand(
        algorithm=algorithm,
        length=length,
        info=hkdf_label(label, length),
        backend=backend
    ).derive(secret)


def derive_keying_material(cid, is_client):
    if is_client:
        label = b'client in'
    else:
        label = b'server in'
    secret = HKDF(
        algorithm=algorithm,
        length=32,
        salt=INITIAL_SALT,
        info=hkdf_label(label, 32),
        backend=backend
    ).derive(cid)
    key = hkdf_expand_label(secret, b'quic key', 16)
    iv = hkdf_expand_label(secret, b'quic iv', 12)
    hp = hkdf_expand_label(secret, b'quic hp', 16)
    return key, iv, hp


def encrypt_packet(key, iv, hp, plain_header, plain_payload):
    pn_length = (plain_header[0] & 0x03) + 1
    pn_offset = len(plain_header) - pn_length
    pn = plain_header[pn_offset:pn_offset + pn_length]

    # payload protection
    nonce = bytearray(len(iv) - pn_length) + bytearray(pn)
    for i in range(len(iv)):
        nonce[i] ^= iv[i]
    aesgcm = aead.AESGCM(key)
    protected_payload = aesgcm.encrypt(nonce, plain_payload, plain_header)

    # header protection
    sample_offset = 4 - pn_length
    sample = protected_payload[sample_offset:sample_offset + 16]
    cipher = Cipher(algorithms.AES(hp), modes.ECB(), backend=backend)
    encryptor = cipher.encryptor()
    buf = bytearray(31)
    encryptor.update_into(sample, buf)
    mask = buf[:5]

    packet = bytearray(plain_header + protected_payload)
    if is_long_header(packet[0]):
        # long header
        packet[0] ^= (mask[0] & 0x0f)
    else:
        # short header
        packet[0] ^= (mask[0] & 0x1f)

    for i in range(pn_length):
        packet[pn_offset + i] ^= mask[1 + i]

    return packet