SBOX = [0x5, 0xC, 0xF, 0x2, 0x0, 0x9, 0x3, 0x4, 0xA, 0x7, 0x6, 0x1, 0xD, 0xE, 0x8, 0xB]

MASK32 = 0xFFFFFFFF

def rotl32(x, n):
    n &= 31
    return ((x << n) | (x >> (32 - n))) & MASK32


def substitution(x):
    out = 0
    for i in range(8):
        shift = (7 - i) * 4
        nibble = (x >> shift) & 0xF
        out |= SBOX[nibble] << shift
    return out


def ROT(t):
    return t ^ rotl32(t, 4) ^ rotl32(t, 8) ^ rotl32(t, 12)


def F(x, rk):
    t = (x ^ rk) & MASK32
    t = substitution(t)
    return ROT(t)