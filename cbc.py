import os

from cipher import encrypt_block, decrypt_block



def xor(a, b):
    return bytes(x ^ y for x, y in zip(a, b))

# CBC (Cipher Block Chaining): C_i = E(P_i xor C_{i-1}), C_0 = IV
# Input sudah di-padding. Output = IV || C, IV acak 16 byte kalau tidak diberikan
def encrypt(p, K, iv=None):
    if iv is None:
        iv = os.urandom(16)
    if len(iv) != 16:
        raise ValueError("IV must be exactly 16 bytes")
    prev = iv
    C = b''
    for i in range(0, len(p), 16):
        prev = encrypt_block(xor(p[i:i+16], prev), K)
        C += prev
    return iv + C

# P_i = D(C_i) xor C_{i-1}, IV diambil dari 16 byte pertama
def decrypt(C, K):
    if len(C) < 32 or len(C) % 16:
        raise ValueError("Ciphertext must be IV + complete 16-byte blocks")
    prev, C = C[:16], C[16:]
    p = b''
    for i in range(0, len(C), 16):
        block = C[i:i+16]
        p += xor(decrypt_block(block, K), prev)
        prev = block
    return p
