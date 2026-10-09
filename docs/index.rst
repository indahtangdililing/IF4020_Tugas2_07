SONI-128 API Documentation
=========================

Dokumentasi API untuk **SONI-128**, implementasi block cipher 128-bit dengan Python 
beserta mode operasi ECB, CBC, CFB, OFB, dan Counter, yang dibuat untuk
*Tugas 2 IF4020 Kriptografi* oleh Kelompok 07 (NIM 13523047, 13523053, 13523120, 13523121).

Deskripsi API
-------------

API ini adalah dokumentasi Python untuk mengenkripsi dan mendekripsi data biner
(``bytes``) menggunakan block cipher SONI-128. Seluruh fungsi bersifat *pure function*
dan tidak membutuhkan library pihak ketiga.

.. list-table:: Spesifikasi cipher
   :header-rows: 1
   :widths: 30 70

   * - Properti
     - Nilai
   * - Ukuran blok
     - 128 bit (16 byte), diperlakukan sebagai 4 *word* 32-bit *big-endian*
   * - Ukuran kunci
     - 128 bit (16 byte)
   * - Jumlah ronde
     - 18 (konstanta ``cipher.ROUNDS``)
   * - Struktur
     - Jaringan Feistel umum 4 cabang dengan fungsi ``F`` (S-box 4-bit + difusi rotasi),
       permutasi antar-cabang ``RP``, dan *mixing layer* ``ML`` setiap 6 ronde
   * - Padding
     - PKCS #7 (selalu menambahkan 1 sampai 16 byte)
   * - Mode operasi
     - ECB, CBC, CFB (``s`` = 8..128 bit), OFB (``s`` = 8..128 bit), CTR

Peta modul
----------

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Modul
     - Fungsi
   * - :py:mod:`soni128`
     - **API high level**: ``encrypt``, ``decrypt``, ``padding``, ``unpad``
   * - ``ecb``, ``cbc``, ``cfb``, ``ofb``, ``ctr``
     - API per mode operasi, lihat :doc:`modes`
   * - ``cipher``
     - Enkripsi/dekripsi **satu blok** 16 byte, lihat :doc:`cipher`
   * - ``key_schedule``, ``f``, ``mixing_layer``, ``rp``
     - Komponen internal cipher, lihat :doc:`internals`
   * - ``main``
     - Program CLI interaktif, lihat :doc:`cli`

Instalasi dan kebutuhan
-----------------------

Tidak ada instalasi paket.Clone repositori lalu jalankan Python 3.10+
dari dalam direktori proyek:

.. code-block:: console

   $ git clone https://github.com/indahtangdililing/IF4020_Tugas2_07
   $ cd IF4020_Tugas2_07

Library eksternal ``pandas`` dan ``matplotlib`` (``requirements.txt`` repositori)
hanya dibutuhkan oleh ``uji_keamanan.py`` untuk membuat tabel dan histogram
pengujian, bukan oleh cipher itu sendiri.

Mulai cepat
-----------

.. code-block:: python

   from soni128 import encrypt, decrypt

   key = b"0123456789abcdef"            # tepat 16 byte
   ciphertext = encrypt(b"Halo, dunia!", key, "cbc")
   plaintext = decrypt(ciphertext, key, "cbc")
   assert plaintext == b"Halo, dunia!"

.. toctree::
   :maxdepth: 2
   :caption: Referensi API

   soni128
   modes
   cipher
   internals
   cli
   examples
   notes
