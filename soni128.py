import cbc
import ecb

# PKCS #7 padding
def padding(plaintext):
    len_bytes = len(plaintext)
    pad = 16 - len_bytes % 16
    return plaintext + bytes([pad]) * pad

def unpad(plaintext):
    if not plaintext or len(plaintext) % 16:
        raise ValueError("Invalid PKCS#7 padding")
    pad = plaintext[-1]
    if not 1 <= pad <= 16 or plaintext[-pad:] != bytes([pad]) * pad:
        raise ValueError("Invalid PKCS#7 padding")
    return plaintext[:-pad]

def encrypt(P, K, mode="ecb"):
    p = padding(P)
    if mode == "cbc":
        return cbc.encrypt(p, K)
    return ecb.encrypt(p, K)

def decrypt(C, K, mode="ecb"):
    p = cbc.decrypt(C, K) if mode == "cbc" else ecb.decrypt(C, K)
    return unpad(p)
