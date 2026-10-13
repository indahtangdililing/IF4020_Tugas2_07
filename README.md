# SONI-128

Tugas 2 IF4020 Kriptografi oleh Kelompok 07 
- Indah Novita Tangdililing 13523047 
- Sakti Bimasena 13523053
- Bevinda Vivian 13523120 
- Ahmad Wicaksono 13523121

**Dokumentasi API:** <https://if-4020-tugas2-07.vercel.app/>

## Deskripsi Program

SONI-128 adalah implementasi *block cipher* 128-bit dalam Python beserta mode operasi
ECB, CBC, CFB, OFB, dan Counter (CTR). Program dapat dipakai sebagai library Python
untuk mengenkripsi/mendekripsi data `bytes`, maupun lewat program CLI untuk
mengenkripsi/mendekripsi berkas `.txt`.

| Properti     | Nilai                                                                                   |
| ------------ | --------------------------------------------------------------------------------------- |
| Ukuran blok  | 128 bit (16 byte)                                                                       |
| Ukuran kunci | 128 bit (16 byte)                                                                       |
| Jumlah ronde | 6                                                                                       |
| Struktur     | Jaringan Feistel 4 cabang: fungsi `F` (S-box 4-bit + difusi rotasi), permutasi `RP`, dan *mixing layer* `ML` setiap 3 ronde (setelah ronde 3 dan 6) |
| Padding      | PKCS #7                                                                                 |
| Mode operasi | ECB, CBC, CFB, OFB, CTR                                                                 |

Diagram arsitektur, ronde, dan *key schedule* tersedia laporan lengkap di
[`docs/13523047_13523053_13523120_13523121_Tugas2_IF4020.pdf`](docs/13523047_13523053_13523120_13523121_Tugas2_IF4020.pdf).

## Tech Stack

- **Python 3.10+** — implementasi cipher, mode operasi, dan CLI (hanya standard library)
- **pandas** & **matplotlib** — pengujian keamanan (tabel dan histogram)
- **Sphinx** + tema **Furo** — dokumentasi API
- **Vercel** — hosting dokumentasi API

## Dependensi

| Kebutuhan                          | Dependensi                         | Berkas                                       |
| ---------------------------------- | ---------------------------------- | -------------------------------------------- |
| Enkripsi/dekripsi (library & CLI)  | Tidak ada (Python standard library) | –                                            |
| Pengujian keamanan (`uji_keamanan.py`) | `pandas`, `matplotlib`         | [`requirements.txt`](requirements.txt)       |
| Build dokumentasi                  | `sphinx>=7.0`, `furo`              | [`docs/requirements.txt`](docs/requirements.txt) |

## Cara Menjalankan Program

### 1. Clone repositori

```bash
git clone https://github.com/indahtangdililing/IF4020_Tugas2_07
cd IF4020_Tugas2_07
```

### 2. Program CLI

```bash
python main.py
```

Program akan meminta masukan secara berurutan:

```
Mode (encrypt/decrypt): encrypt
Block mode (ecb/cbc/cfb/ofb/ctr): cbc
Input .txt file: pesan.txt
Key (16 UTF-8 bytes): 0123456789abcdef
Saved to pesan.encrypted.txt
```

- `encrypt` menghasilkan `<nama>.encrypted.txt` berisi ciphertext dalam heksadesimal.
- `decrypt` menerima berkas heksadesimal tersebut dan menghasilkan `<nama>.decrypted.txt`.
- Berkas keluaran yang sudah ada tidak akan ditimpa.


### 3. Sebagai library Python

```python
from soni128 import encrypt, decrypt

key = b"0123456789abcdef"  # tepat 16 byte
ciphertext = encrypt(b"Halo, dunia!", key, "cbc")
plaintext = decrypt(ciphertext, key, "cbc")
assert plaintext == b"Halo, dunia!"
```

### 4. Pengujian

Pengujian fungsional:

```bash
python test_soni128.py
```

Pengujian keamanan (efek avalanche, entropi, dan histogram; hasil disimpan di `hasil_uji/`):

```bash
pip install -r requirements.txt
python uji_keamanan.py [berkas_plaintext]
```

### 5. Build dokumentasi API secara lokal

```bash
pip install -r docs/requirements.txt
sphinx-build -b html docs docs/_build/html
```

Buka `docs/_build/html/index.html` di browser.
