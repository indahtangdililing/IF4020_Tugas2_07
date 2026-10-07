from f import F
from key_schedule import key_schedule, is_ml
from mixing_layer import ML, ML_inv
from rp import RP, RP_inv

ROUNDS = 18


def to_words(b):
    return [int.from_bytes(b[i:i + 4], "big") for i in range(0, 16, 4)]


def to_bytes(w):
    return b"".join(x.to_bytes(4, "big") for x in w)


def encrypt_block(block, key, R=ROUNDS):
    assert len(block) == 16, "blok harus 16 byte"
    wk, rk, mk = key_schedule(key, R)
    x = [a ^ b for a, b in zip(to_words(block), wk[:4])]
    j = 0
    for r in range(R):
        x[1] ^= F(x[0], rk[2 * r])
        x[3] ^= F(x[2], rk[2 * r + 1])
        x = list(RP(*x))
        if is_ml(r, R):
            x = list(ML(*x, mk[j:j + 4]))
            j += 4
    return to_bytes(a ^ b for a, b in zip(x, wk[4:]))


def decrypt_block(block, key, R=ROUNDS):
    assert len(block) == 16, "blok harus 16 byte"
    wk, rk, mk = key_schedule(key, R)
    x = [a ^ b for a, b in zip(to_words(block), wk[4:])]
    j = len(mk)
    for r in reversed(range(R)):
        if is_ml(r, R):
            j -= 4
            x = list(ML_inv(*x, mk[j:j + 4]))
        x = list(RP_inv(*x))
        x[1] ^= F(x[0], rk[2 * r])
        x[3] ^= F(x[2], rk[2 * r + 1])
    return to_bytes(a ^ b for a, b in zip(x, wk[:4]))
