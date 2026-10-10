from cipher import encrypt_block, decrypt_block


# ECB (Electronic CodeBook): tiap blok dienkripsi sendiri-sendiri
# Input sudah padding (kelipatan 16 byte)
def encrypt(p, K):
    C = b''
    for i in range(0, len(p), 16):
        C += encrypt_block(p[i:i+16], K)
    return C

def decrypt(C, K):
    if not C or len(C) % 16:
        raise ValueError("Ciphertext must contain complete 16-byte blocks") # format fix block
    p = b''
    for i in range(0, len(C), 16):
        p += decrypt_block(C[i:i+16], K)
    return p
