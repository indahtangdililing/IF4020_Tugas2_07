MASK16 = 0xFFFF
MASK32 = 0xFFFFFFFF


def rotl16(x, n):
    n &= 15
    return ((x << n) | (x >> (16 - n))) & MASK16


def rotr16(x, n):
    n &= 15
    return ((x >> n) | (x << (16 - n))) & MASK16


def split(x):
    # pecah 16 | 16
    return (x >> 16) & MASK16, x & MASK16


def join(hi, lo):
    return ((hi & MASK16) << 16) | (lo & MASK16)


def ML(x0, x1, x2, x3, mk, mk2=None):
    # mk   4 word 32-bit (K1..K4) dari key schedule
    # mk2  opsional di 4 word 32-bit untuk output whitening
    x0, x1, x2, x3 = x0 ^ mk[0], x1 ^ mk[1], x2 ^ mk[2], x3 ^ mk[3]

    b1, b2 = split(x0)
    b3, b4 = split(x1)
    b5, b6 = split(x2)
    b7, b8 = split(x3)

    b1 = rotl16((b1 + b3) & MASK16, 1)
    b2 = rotl16(b2 ^ b4, 3)
    b8 = rotl16((b8 + b1) & MASK16, 5)
    b3 = rotl16(b3 ^ b5, 7)
    b7 = rotl16((b7 + b2) & MASK16, 9)
    b4 = rotl16(b4 ^ b6, 11)
    b6 = rotl16((b6 + b3) & MASK16, 13)
    b5 = rotl16(b5 ^ b7, 2)
    b5 = rotl16((b5 + b4) & MASK16, 6)
    b6 = rotl16(b6 ^ b8, 10)

    y0, y1, y2, y3 = join(b1, b5), join(b2, b6), join(b3, b7), join(b4, b8)

    if mk2 is not None:
        y0, y1, y2, y3 = y0 ^ mk2[0], y1 ^ mk2[1], y2 ^ mk2[2], y3 ^ mk2[3]
    return y0, y1, y2, y3


def ML_inv(y0, y1, y2, y3, mk, mk2=None):
    # kebalikan ML
    if mk2 is not None:
        y0, y1, y2, y3 = y0 ^ mk2[0], y1 ^ mk2[1], y2 ^ mk2[2], y3 ^ mk2[3]

    b1, b5 = split(y0)
    b2, b6 = split(y1)
    b3, b7 = split(y2)
    b4, b8 = split(y3)

    b6 = rotr16(b6, 10) ^ b8
    b5 = (rotr16(b5, 6) - b4) & MASK16
    b5 = rotr16(b5, 2) ^ b7
    b6 = (rotr16(b6, 13) - b3) & MASK16
    b4 = rotr16(b4, 11) ^ b6
    b7 = (rotr16(b7, 9) - b2) & MASK16
    b3 = rotr16(b3, 7) ^ b5
    b8 = (rotr16(b8, 5) - b1) & MASK16
    b2 = rotr16(b2, 3) ^ b4
    b1 = (rotr16(b1, 1) - b3) & MASK16

    x0, x1, x2, x3 = join(b1, b2), join(b3, b4), join(b5, b6), join(b7, b8)
    return x0 ^ mk[0], x1 ^ mk[1], x2 ^ mk[2], x3 ^ mk[3]
