MASK = 0xFFFFFFFF


def rotl(x, n):
    return ((x << n) | (x >> (32 - n))) & MASK


def rotr(x, n):
    return ((x >> n) | (x << (32 - n))) & MASK


def is_ml(r, R):
    return (r + 1) % 6 == 0 and r != R - 1


def key_stream(key):
    k, l0, l1, l2 = (int.from_bytes(key[j:j + 4], "big") for j in range(0, 16, 4))
    i = 0
    while True:
        x = ((rotr(l0, 8) + k) & MASK) ^ i
        k = rotl(k, 3) ^ x
        l0, l1, l2 = l1, l2, x
        i += 1
        yield k


def key_schedule(key, R):
    assert len(key) == 16, "kunci harus 16 byte"
    assert R >= 4, "R harus >= 4"

    ks = key_stream(key)
    for _ in range(8):
        next(ks)

    wk = [next(ks) for _ in range(4)]
    rk, mk = [], []
    for r in range(R):
        rk += [next(ks), next(ks)]
        if is_ml(r, R):
            mk += [next(ks) for _ in range(4)]
    wk += [next(ks) for _ in range(4)]
    return wk, rk, mk
