from cipher import encrypt_block, decrypt_block

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

def encrypt(P, K):
    p = padding(P)
    C = b''
    for i in range(0, len(p), 16):
        C += encrypt_block(p[i:i+16], K)
    return C

def decrypt(C, K):
    p = b''
    for i in range(0, len(C), 16):
        p += decrypt_block(C[i:i+16], K)
    return unpad(p)
