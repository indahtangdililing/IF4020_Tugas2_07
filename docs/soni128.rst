Modul ``soni128`` (API high level)
======================================

.. py:module:: soni128

Antarmuka utama yang sebaiknya dipakai. Modul ini menangani padding PKCS #7 dan memilih
mode operasi. Untuk mode selain ECB, IV/counter acak 16 byte dibuat otomatis dan
ditempelkan di depan ciphertext.

.. py:data:: STREAM
   :type: dict[str, module]

   Pemetaan nama mode ke modulnya: ``{"cbc": cbc, "cfb": cfb, "ofb": ofb, "ctr": ctr}``.
   ECB tidak ada di sini; ECB dipakai sebagai mode bawaan.

.. py:function:: encrypt(P: bytes, K: bytes, mode: str = "ecb") -> bytes

   Mengenkripsi ``P`` dengan kunci ``K``. ``P`` di-padding PKCS #7 terlebih dahulu
   untuk semua mode.

   :param P: Plaintext, panjang bebas (boleh kosong).
   :type P: bytes
   :param K: Kunci, tepat 16 byte.
   :type K: bytes
   :param mode: Mode operasi: ``"ecb"``, ``"cbc"``, ``"cfb"``, ``"ofb"``, atau ``"ctr"``
      (huruf kecil).
   :type mode: str
   :returns: Ciphertext. Panjangnya ``16 * (len(P) // 16 + 1)`` byte untuk ECB, dan
      ``16 + 16 * (len(P) // 16 + 1)`` byte untuk CBC/CFB/OFB/CTR (16 byte pertama = IV/counter).
   :rtype: bytes
   :raises AssertionError: jika ``len(K) != 16``.

   .. note::
      Parameter ``iv``, ``counter``, dan ``s`` pada modul mode tidak diteruskan oleh fungsi ini.
      IV selalu acak dan ``s`` selalu 8 bit. Untuk mengatur keduanya, panggil modul mode
      secara langsung (lihat :doc:`modes`).

.. py:function:: decrypt(C: bytes, K: bytes, mode: str = "ecb") -> bytes

   Mendekripsi ``C`` dan membuang padding. ``mode`` harus sama dengan saat enkripsi.

   :param C: Ciphertext hasil :py:func:`encrypt`. Untuk CBC/CFB/OFB/CTR, 16 byte pertama
      dibaca sebagai IV/counter.
   :type C: bytes
   :param K: Kunci, tepat 16 byte.
   :type K: bytes
   :param mode: Mode operasi, sama seperti pada :py:func:`encrypt`.
   :type mode: str
   :returns: Plaintext asli tanpa padding.
   :rtype: bytes
   :raises ValueError: jika panjang ciphertext bukan kelipatan 16 byte atau kosong (ECB),
      jika ciphertext CBC lebih pendek dari 32 byte, atau jika padding PKCS #7 tidak valid
      (biasanya karena kunci atau mode salah).
   :raises AssertionError: jika ``len(K) != 16``.

.. py:function:: padding(plaintext: bytes) -> bytes

   Menambahkan padding PKCS #7. Jika panjang sudah kelipatan 16, ditambahkan satu blok
   penuh (16 byte bernilai ``0x10``).

   :param plaintext: Data yang akan di-padding.
   :type plaintext: bytes
   :returns: Data dengan panjang kelipatan 16; ``n`` byte terakhir bernilai ``n`` (1 ≤ n ≤ 16).
   :rtype: bytes

.. py:function:: unpad(plaintext: bytes) -> bytes

   Membuang padding PKCS #7 dan memvalidasinya.

   :param plaintext: Data ber-padding, panjang kelipatan 16 dan tidak kosong.
   :type plaintext: bytes
   :returns: Data tanpa padding.
   :rtype: bytes
   :raises ValueError: jika data kosong, panjang bukan kelipatan 16, byte terakhir di luar 1..16,
      atau byte padding tidak konsisten.
