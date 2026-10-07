import sys
from collections import Counter
from math import log2
from pathlib import Path
from statistics import mean

import pandas as pd
from matplotlib import pyplot as plt

from soni128 import STREAM, decrypt, ecb, encrypt, padding


def flip(data, bit):
    data = bytearray(data)
    data[bit // 8] ^= 1 << (bit % 8)
    return bytes(data)


def beda(a, b):
    assert len(a) == len(b) and a
    return sum((x ^ y).bit_count() for x, y in zip(a, b)) / (8 * len(a)) * 100


def entropi(data):
    return -sum(n / len(data) * log2(n / len(data)) for n in Counter(data).values())


def enkripsi(data, key, mode):
    # IV/counter tetap hanya untuk pengujian, supaya perbandingan adil.
    if mode == "ecb":
        return ecb.encrypt(padding(data), key)
    return STREAM[mode].encrypt(padding(data), key, bytes(range(16)))


def histogram(plaintext, ciphertext, file):
    data = pd.DataFrame({"Plaintext": pd.Series(list(plaintext)),
                         "Ciphertext": pd.Series(list(ciphertext))})
    axes = data.plot.hist(bins=range(257), density=True, subplots=True,
                          layout=(1, 2), figsize=(12, 4), legend=False,
                          title=["Plaintext", "Ciphertext"])
    for ax in axes.flat:
        ax.set(xlim=(0, 256), xlabel="Nilai byte", ylabel="Frekuensi relatif")
        ax.axhline(1 / 256, color="red", linestyle="--")
    fig = axes.flat[0].figure
    fig.suptitle(file.stem.upper())
    fig.tight_layout()
    fig.savefig(file, dpi=150)
    plt.close(fig)


if __name__ == "__main__":
    # Teks berulang sengaja dipakai supaya pola ECB terlihat.
    plaintext = Path(sys.argv[1]).read_bytes() if len(sys.argv) > 1 else (b"Pengujian block cipher SONI128.\n" * 600)[:16384]
    if not plaintext:
        raise SystemExit("Berkas kosong: histogram plaintext tidak dapat dihitung.")
    key = b"0123456789abcdef"
    sample = bytes(range(15))  # Setelah padding tepat satu blok, tanpa blok padding tambahan.
    output = Path("hasil_uji")
    output.mkdir(exist_ok=True)

    assert entropi(b"aaaa") == 0 and entropi(bytes(range(256))) == 8
    assert beda(bytes(16), flip(bytes(16), 0)) == 100 / 128
    lines = ["Mode   AE plaintext   AE kunci   Entropi ciphertext"]
    for mode in ("ecb", "cbc", "cfb", "ofb", "ctr"):
        offset = 0 if mode == "ecb" else 16
        base = enkripsi(sample, key, mode)[offset:]
        ae_p = [beda(base, enkripsi(flip(sample, bit), key, mode)[offset:]) for bit in range(120)]
        ae_k = [beda(base, enkripsi(sample, flip(key, bit), mode)[offset:]) for bit in range(128)]
        ciphertext = enkripsi(plaintext, key, mode)
        assert decrypt(ciphertext, key, mode) == plaintext, f"Dekripsi {mode} gagal"
        for size in (0, 1, 15, 16, 17, 33):
            data = bytes(range(size))
            assert decrypt(encrypt(data, key, mode), key, mode) == data, f"{mode}, {size} byte"
        payload = ciphertext[offset:]
        lines.append(f"{mode.upper():5} {mean(ae_p):11.2f}% {mean(ae_k):9.2f}% {entropi(payload):18.4f}")
        histogram(plaintext, payload, output / f"{mode}.png")

    report = "\n".join(lines)
    print(report)
    (output / "hasil.txt").write_text(report + "\n", encoding="utf-8")
