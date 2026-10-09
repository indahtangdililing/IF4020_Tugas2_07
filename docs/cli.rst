Program CLI (``main.py``)
=========================

Program untuk mengenkripsi atau mendekripsi txt dari terminal.

.. code-block:: console

   $ python3 main.py

Masukan (dibaca berurutan lewat ``input()``)
--------------------------------------------

.. list-table::
   :header-rows: 1
   :widths: 24 16 60

   * - Prompt
     - Tipe
     - Penjelasan
   * - ``Mode (encrypt/decrypt)``
     - str
     - ``encrypt`` atau ``decrypt`` (huruf besar/kecil diabaikan).
   * - ``Block mode``
     - str
     - ``ecb``, ``cbc``, ``cfb``, ``ofb``, atau ``ctr``.
   * - ``Input .txt file``
     - path (str)
     - Saat ``encrypt``, isi dibaca sebagai byte mentah. Saat ``decrypt``,
       isi harus berupa teks heksadesimal ASCII hasil enkripsi.
   * - ``Key (16 UTF-8 bytes)``
     - str
     - Kunci, hasil encode UTF-8 harus tepat 16 byte (karakter non-ASCII memakai lebih dari 1 byte).

Keluaran
--------

.. list-table::
   :header-rows: 1
   :widths: 20 40 40

   * - Mode
     - Document output
     - Isi
   * - ``encrypt``
     - ``<nama>.encrypted.txt``
     - Ciphertext dalam heksadesimal (teks ASCII)
   * - ``decrypt``
     - ``<nama>.decrypted.txt``
     - Plaintext asli (byte mentah)

Ekstensi ``.txt`` pada input diganti. Contoh: mendekripsi ``pesan.encrypted.txt``
menghasilkan ``pesan.encrypted.decrypted.txt``. Output dibuat untuk menolak menimpa txt yang sudah ada.

Kode keluar dan pesan error
---------------------------

Berhasil akan muncul ``Saved to <document>``. Jika gagal akan muncul ``Error: <pesan>``.

.. list-table::
   :header-rows: 1
   :widths: 45 55

   * - Pesan
     - Penyebab
   * - ``Mode must be encrypt or decrypt``
     - Mode salah.
   * - ``Block mode must be ecb/cbc/cfb/ofb/ctr``
     - Mode blok salah.
   * - ``Key must be exactly 16 bytes``
     - Panjang kunci (dalam byte UTF-8) bukan 16.
   * - ``Ciphertext must contain complete 16-byte blocks``
     - Saat ``decrypt``, hasil konversi heksadesimal kosong atau bukan kelipatan 16 byte.
   * - ``non-hexadecimal number found in fromhex() ...``
     - Saat ``decrypt``, isi input bukan teks heksadesimal yang valid.
   * - ``Invalid PKCS#7 padding``
     - Kunci atau mode dekripsi salah.
   * - ``[Errno 2] No such file or directory: ...``
     - Input tidak ditemukan.
   * - ``[Errno 17] File exists: ...``
     - Output sudah ada.
