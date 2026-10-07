from pathlib import Path

from soni128 import encrypt, decrypt


def main():
    try:
        mode = input("Mode (encrypt/decrypt): ").strip().lower()
        if mode not in ("encrypt", "decrypt"):
            raise ValueError("Mode must be encrypt or decrypt")
        source = Path(input("Input .txt file: ").strip()).expanduser()
        key = input("Key (16 UTF-8 bytes): ").encode("utf-8")
        if len(key) != 16:
            raise ValueError("Key must be exactly 16 bytes")

        if mode == "encrypt":
            result = encrypt(source.read_bytes(), key).hex().encode("ascii")
        else:
            ciphertext = bytes.fromhex(source.read_text(encoding="ascii"))
            if not ciphertext or len(ciphertext) % 16:
                raise ValueError("Ciphertext must contain complete 16-byte blocks")
            result = decrypt(ciphertext, key)

        output = source.with_suffix(".encrypted.txt" if mode == "encrypt" else ".decrypted.txt")
        with output.open("xb") as file:
            file.write(result)
        print(f"Saved to {output}")
    except (OSError, ValueError) as error:
        raise SystemExit(f"Error: {error}")


if __name__ == "__main__":
    main()
