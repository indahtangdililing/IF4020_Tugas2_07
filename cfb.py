import os

from cipher import encrypt_block


def xor(a, b):
    return bytes(x ^ y for x, y in zip(a, b))

# CFB (Cipher Feedback)
#   C_j     = P_j xor MSB_s(E_K(X_j))
#   X_{j+1} = LSB_{b-s}(X_j) || C_j,   X_1 = IV
# Output = IV || C, IV acak 16 byte kalau tidak diberikan
def encrypt(p, K, iv=None, s=8):
    n = _unit_bytes(s)
    if iv is None:
        iv = os.urandom(16)
    if len(iv) != 16:
        raise ValueError("IV must be exactly 16 bytes")
    X = iv
    C = b''
    for i in range(0, len(p), n):
        unit = p[i:i+n]
        c = xor(unit, encrypt_block(X, K)[:len(unit)])  # MSB_s(E_K(X_j))
        C += c
        X = X[n:] + c  # geser antrian n byte ke kiri, + C_j di kanan
    return iv + C

# P_j = C_j xor MSB_s(E_K(X_j)). Formula decrypt CFB juga memakai E,
# IV dari 16 byte pertama
def decrypt(C, K, s=8):
    n = _unit_bytes(s)
    if len(C) < 16:
        raise ValueError("Ciphertext must start with a 16-byte IV")
    X, C = C[:16], C[16:]
    p = b''
    for i in range(0, len(C), n):
        c = C[i:i+n]
        p += xor(c, encrypt_block(X, K)[:len(c)])
        X = X[n:] + c 
    return p

def _unit_bytes(s):
    if s % 8 or not 8 <= s <= 128:
        raise ValueError("s must be a multiple of 8 between 8 and 128")
    return s // 8