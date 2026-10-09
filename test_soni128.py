from pathlib import Path
from random import Random
from tempfile import TemporaryDirectory
from unittest.mock import patch

from cipher import encrypt_block
from main import main
from soni128 import padding, unpad, encrypt, decrypt


if __name__ == "__main__":
    for length, expected_padding in (
        (0, b"\x10" * 16),
        (1, b"\x0f" * 15),
        (15, b"\x01"),
        (16, b"\x10" * 16),
        (17, b"\x0f" * 15),
        (32, b"\x10" * 16),
    ):
        plaintext = b"a" * length
        assert padding(plaintext) == plaintext + expected_padding
        assert unpad(padding(plaintext)) == plaintext
        assert decrypt(encrypt(plaintext, bytes(16)), bytes(16)) == plaintext

    for malformed in (
        b"",
        b"\x01",
        b"a" * 15 + b"\x00",
        b"\x11" * 16,
        b"a" * 15 + b"\x02",
    ):
        try:
            unpad(malformed)
        except ValueError:
            pass
        else:
            raise AssertionError(f"Accepted invalid padding: {malformed!r}")

    rng = Random(128)
    messages = [rng.randbytes(length) for length in range(66)]
    messages += [rng.randbytes(rng.randrange(1025)) for _ in range(100)]
    messages += [bytes(256), b"\xff" * 256, bytes(range(256)), "Hello, world! 🔐".encode()]
    for plaintext in messages:
        key = rng.randbytes(16)
        padded = padding(plaintext)
        ciphertext = encrypt(plaintext, key)
        assert len(ciphertext) == (len(plaintext) // 16 + 1) * 16
        assert ciphertext == b"".join(
            encrypt_block(padded[i:i + 16], key)
            for i in range(0, len(padded), 16)
        )
        assert unpad(padded) == plaintext
        assert decrypt(ciphertext, key) == plaintext

    invalid_calls = [
        (decrypt, (b"", bytes(16)), ValueError),
        (decrypt, (encrypt_block(b"a" * 15 + b"\x00", bytes(16)), bytes(16)), ValueError),
    ]
    for length in (1, 15, 17, 31):
        invalid_calls.append((decrypt, (bytes(length), bytes(16)), ValueError))
    for length in (0, 1, 15, 17, 32):
        invalid_calls.append((encrypt, (b"hello", bytes(length)), AssertionError))
        invalid_calls.append((decrypt, (bytes(16), bytes(length)), AssertionError))
    for function, args, error in invalid_calls:
        try:
            function(*args)
        except error:
            pass
        else:
            raise AssertionError(f"{function.__name__} accepted invalid input: {args!r}")

    with TemporaryDirectory() as directory:
        # directory = "."  buat liat langsung not di temp
        source = Path(directory) / "message.txt"
        plaintext = "Hello, world! 🔐\n".encode("utf-8")
        source.write_bytes(plaintext)
        with patch("builtins.input", side_effect=("encrypt", "ecb", str(source), "0123456789abcdef")):
            main()
        encrypted = source.with_suffix(".encrypted.txt")
        assert bytes.fromhex(encrypted.read_text()) == encrypt(plaintext, b"0123456789abcdef")
        with patch("builtins.input", side_effect=("decrypt", "ecb", str(encrypted), "0123456789abcdef")):
            main()
        assert encrypted.with_suffix(".decrypted.txt").read_bytes() == plaintext
        assert source.read_bytes() == plaintext

    print(f"Passed: padding boundaries, {len(messages)} round trips, invalid inputs, and file encryption/decryption.")
