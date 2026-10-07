import os

from cipher import encrypt_block


def xor(a, b):
    return bytes(x ^ y for x, y in zip(a, b))

# OFB (Output Feedback) 
#   O_j     = E_K(X_j),  X_1 = IV
#   C_j     = P_j xor MSB_s(O_j)
#   X_{j+1} = LSB_{b-s}(X_j) || MSB_s(O_j)
# OFB mirip CFB, bedanya ntar ditambahin ulang itu s-bit hasil enkripsi bukan cipherteks
# enkripsi = dekripsi (XOR with keystream yang sama).
# Kalau s = 128 (s = b) maka X_{j+1} = E_K(X_j)
# Output = IV || C, IV acak 16 byte kalau tidak diberikan
def encrypt(p, K, iv=None, s=8):
    if iv is None:
        iv = os.urandom(16)
    if len(iv) != 16:
        raise ValueError("IV must be exactly 16 bytes")
    return iv + ofb(p, K, iv, s)

# IV diambil dari 16 byte pertama, lalu XOR dengan keystream yang sama
def decrypt(C, K, s=8):
    if len(C) < 16:
        raise ValueError("Ciphertext must start with a 16-byte IV")
    return ofb(C[16:], K, C[:16], s)

def ofb(data, K, iv, s):
    if s % 8 or not 8 <= s <= 128:
        raise ValueError("s must be a multiple of 8 between 8 and 128")
    n = s // 8
    X = iv
    out = b''
    for i in range(0, len(data), n):
        unit = data[i:i+n]
        k = encrypt_block(X, K)[:n]  # MSB_s(E_K(X_j))
        out += xor(unit, k)
        X = X[n:] + k  # bedanya sama cfb ini + keystream
    return out