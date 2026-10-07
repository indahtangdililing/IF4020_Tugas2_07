from pathlib import Path

from soni128 import encrypt, decrypt


try:
    mode = input("Mode (encrypt/decrypt): ").strip().lower()
    if mode not in ("encrypt", "decrypt"):
        raise ValueError("Mode must be encrypt or decrypt")
    block_mode = input("Block mode (ecb/cbc/cfb/ofb/ctr): ").strip().lower()
    if block_mode not in ("ecb", "cbc", "cfb", "ofb", "ctr"):
        raise ValueError("Block mode must be ecb/cbc/cfb/ofb/ctr")
    source = Path(input("Input .txt file: ").strip()).expanduser()
    key = input("Key (16 UTF-8 bytes): ").encode("utf-8")
    if len(key) != 16:
        raise ValueError("Key must be exactly 16 bytes")

    if mode == "encrypt":
        result = encrypt(source.read_bytes(), key, block_mode).hex().encode("ascii")
    else:
        ciphertext = bytes.fromhex(source.read_text(encoding="ascii"))
        if not ciphertext or len(ciphertext) % 16:
            raise ValueError("Ciphertext must contain complete 16-byte blocks")
        result = decrypt(ciphertext, key, block_mode)

    output = source.with_suffix(".encrypted.txt" if mode == "encrypt" else ".decrypted.txt")
    with output.open("xb") as file:
        file.write(result)
    print(f"Saved to {output}")
except (OSError, ValueError) as error:
    raise SystemExit(f"Error: {error}")