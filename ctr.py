import os

from cipher import encrypt_block


def xor(a, b):
    return bytes(x ^ y for x, y in zip(a, b))

# Counter Mode (CTR): C_j = P_j xor E_K(T_j), T_{j+1} = T_j + 1 (mod 2^128)
# counter dihitung satu blok (16 byte), nilai awal T_1 acak kalau tidak diberikan.
# tidak perlu padding blok terakhir yang pendek di XOR dengan MSB_u(E_K(T_N)).
# counter awal tidak boleh dipakai ulang dengan kunci yang sama.
# Output = T_1 || C
def encrypt(p, K, counter=None):
    if counter is None:
        counter = os.urandom(16)
    if len(counter) != 16:
        raise ValueError("Counter must be exactly 16 bytes")
    return counter + counter_mode(p, K, counter)

# counter awal diambil dari 16 byte pertama. enkripsi = dekripsi
def decrypt(C, K):
    if len(C) < 16:
        raise ValueError("Ciphertext must start with a 16-byte counter")
    return counter_mode(C[16:], K, C[:16])

def counter_mode(data, K, counter):
    T = int.from_bytes(counter, "big")
    out = b''
    for i in range(0, len(data), 16):
        unit = data[i:i+16]
        keystream = encrypt_block(T.to_bytes(16, "big"), K)
        out += xor(unit, keystream[:len(unit)])  # MSB_u untuk blok terakhir
        T = (T + 1) % (1 << 128)
    return out