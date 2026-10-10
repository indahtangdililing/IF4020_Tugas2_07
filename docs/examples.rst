Contoh penggunaan
=================

Semua output di bawah ini dihasilkan dengan menjalankan kode.
Untuk mode selain ECB, IV/counter dibuat acak, sehingga ciphertext akan berbeda pada setiap
pemanggilan, tapi panjangnya yang tetap.

1. Enkripsi dan dekripsi dengan semua mode
------------------------------------------

.. code-block:: python

   from soni128 import encrypt, decrypt

   key = b"0123456789abcdef"      # 16 byte
   pesan = b"Halo, dunia!"        # 12 byte

   for mode in ("ecb", "cbc", "cfb", "ofb", "ctr"):
       c = encrypt(pesan, key, mode)
       assert decrypt(c, key, mode) == pesan
       print(mode, len(c))

.. code-block:: text

   ecb 16
   cbc 32
   cfb 32
   ofb 32
   ctr 32

ECB menghasilkan 16 byte (satu blok). Mode lain menghasilkan 32 byte: 16 byte IV/counter
ditambah satu blok data dengan padding.

ECB bersifat deterministik, jadi outputnya tetap:

.. code-block:: python

   >>> encrypt(b"Halo, dunia!", b"0123456789abcdef", "ecb").hex()
   '5e8277f5ac9bc847f7cde2795b4d498d'

2. Padding PKCS #7
------------------

.. code-block:: python

   >>> from soni128 import padding, unpad
   >>> padding(b"Halo, dunia!").hex()
   '48616c6f2c2064756e69612104040404'
   >>> unpad(padding(b"Halo, dunia!"))
   b'Halo, dunia!'

Empat byte ``04`` ditambahkan karena 12 byte kurang 4 dari kelipatan 16.

3. Menentukan IV, counter, atau lebar umpan balik ``s``
-------------------------------------------------------

Pakai modul mode langsung, untuk plaintext mode CBC harus dipadding sendiri.

.. code-block:: python

   import cbc, cfb, ctr
   from soni128 import padding

   key = b"0123456789abcdef"
   iv = bytes(range(16))          # 00 01 02 ... 0f

   c = cbc.encrypt(padding(b"Halo, dunia!"), key, iv)
   print(c.hex())
   # 000102030405060708090a0b0c0d0e0fff85b7d7126dd28ac2048b97aec8c6fa

   c = cfb.encrypt(b"abc", key, iv, s=128)
   assert cfb.decrypt(c, key, s=128) == b"abc"

   c = ctr.encrypt(b"abc", key, iv)
   print(c.hex())
   # 000102030405060708090a0b0c0d0e0f94c471

Dua output tetap di atas diawali IV/counter yang diberikan (16 byte), diikuti ciphertext.

4. Enkripsi satu blok
---------------------

.. code-block:: python

   >>> from cipher import encrypt_block, decrypt_block
   >>> key = b"0123456789abcdef"
   >>> blok = bytes(range(16))
   >>> c = encrypt_block(blok, key)
   >>> c.hex()
   'f5a612a19c3f4dc88806f2c69e3f8812'
   >>> decrypt_block(c, key) == blok
   True

5. Penjadwalan kunci / Key scheduling 
--------------------

.. code-block:: python

   >>> from key_schedule import key_schedule, is_ml
   >>> wk, rk, mk = key_schedule(b"0123456789abcdef", 18)
   >>> len(wk), len(rk), len(mk)
   (8, 36, 8)
   >>> [r for r in range(18) if is_ml(r, 18)]
   [5, 11]

6. Penanganan error / Error handling
-------------------

.. code-block:: python

   >>> from soni128 import encrypt, decrypt
   >>> encrypt(b"x", b"pendek")
   AssertionError: kunci harus 16 byte
   >>> decrypt(b"x" * 15, b"0123456789abcdef")
   ValueError: Ciphertext must contain complete 16-byte blocks
   >>> decrypt(bytes(16), b"0123456789abcdef")      # kunci/mode salah
   ValueError: Invalid PKCS#7 padding
   >>> import cfb
   >>> cfb.encrypt(b"a", b"0123456789abcdef", None, 12)
   ValueError: s must be a multiple of 8 between 8 and 128

7. CLI
--------------

.. code-block:: console

   $ printf 'Halo, dunia!' > pesan.txt
   $ python3 main.py
   Mode (encrypt/decrypt): encrypt
   Block mode (ecb/cbc/cfb/ofb/ctr): cbc
   Input .txt file: pesan.txt
   Key (16 UTF-8 bytes): 0123456789abcdef
   Saved to pesan.encrypted.txt
   $ cat pesan.encrypted.txt
   f3add69b4e2c9bec57b74a1febba3789626d4c18ee770d69cf078ec7bfa69ce3
   $ python3 main.py
   Mode (encrypt/decrypt): decrypt
   Block mode (ecb/cbc/cfb/ofb/ctr): cbc
   Input .txt file: pesan.encrypted.txt
   Key (16 UTF-8 bytes): 0123456789abcdef
   Saved to pesan.encrypted.decrypted.txt
   $ cat pesan.encrypted.decrypted.txt
   Halo, dunia!

Pada output heksadesimal, 32 karakter pertama adalah IV acak, sehingga output akan berbeda.
