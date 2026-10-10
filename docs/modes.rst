Mode operasi (``ecb``, ``cbc``, ``cfb``, ``ofb``, ``ctr``)
==========================================================

Setiap mode dirancang pada file terpisah dengan fungsi ``encrypt`` dan ``decrypt`` masing-masing. Tiap mode ini
tidak melakukan padding, karena padding telah dilakukan pada :py:func:`soni128.encrypt`.
Modul ini dapat digunakan langsung jika ingin menentukan IV, counter awal, atau lebar feedback ``s``.

Notasi: ``E_K`` = enkripsi satu blok SONI128 dengan kunci ``K``, ``b`` = 128 (ukuran blok).

ECB
---

.. py:module:: ecb

Setiap blok dienkripsi sendiri-sendiri: ``C_i = E_K(P_i)``.

.. py:function:: encrypt(p: bytes, K: bytes) -> bytes

   :param p: Plaintext yang sudah dipadding (kelipatan 16 byte).
   :type p: bytes
   :param K: Kunci 16 byte.
   :type K: bytes
   :returns: Ciphertext dengan panjang sama dengan ``p``.
   :rtype: bytes
   :raises AssertionError: jika ada blok yang bukan 16 byte atau ``len(K) != 16``.

.. py:function:: decrypt(C: bytes, K: bytes) -> bytes

   :param C: Ciphertext, tidak kosong dan kelipatan 16 byte.
   :type C: bytes
   :param K: Kunci 16 byte.
   :type K: bytes
   :returns: Plaintext masih berpadding, panjang sama dengan ``C``.
   :rtype: bytes
   :raises ValueError: jika ``C`` kosong atau panjangnya bukan kelipatan 16.

CBC
---

.. py:module:: cbc

``C_0 = IV``, ``C_i = E_K(P_i xor C_{i-1})``. Output berformat ``IV || C``.

.. py:function:: encrypt(p: bytes, K: bytes, iv: bytes | None = None) -> bytes

   :param p: Plaintext berpadding (kelipatan 16 byte).
   :type p: bytes
   :param K: Kunci 16 byte.
   :type K: bytes
   :param iv: IV 16 byte. Jika ``None``, dibuat acak dengan ``os.urandom(16)``.
   :type iv: bytes | None
   :returns: ``IV || C``, panjang ``16 + len(p)``.
   :rtype: bytes
   :raises ValueError: jika ``iv`` bukan 16 byte.

.. py:function:: decrypt(C: bytes, K: bytes) -> bytes

   :param C: ``IV || C`` dengan panjang minimal 32 dan kelipatan 16.
   :type C: bytes
   :param K: Kunci 16 byte.
   :type K: bytes
   :returns: Plaintext masih berpadding, panjang ``len(C) - 16``.
   :rtype: bytes
   :raises ValueError: jika panjang ``C`` kurang dari 32 byte atau bukan kelipatan 16.

CFB
---

.. py:module:: cfb

Feedback ``s`` bit: ``C_j = P_j xor MSB_s(E_K(X_j))``, ``X_{j+1} = LSB_{b-s}(X_j) || C_j``,
``X_1 = IV``. Panjang data bebas (tidak perlu padding).

.. py:function:: encrypt(p: bytes, K: bytes, iv: bytes | None = None, s: int = 8) -> bytes

   :param p: Plaintext, panjang bebas.
   :type p: bytes
   :param K: Kunci 16 byte.
   :type K: bytes
   :param iv: IV 16 byte; ``None`` = acak.
   :type iv: bytes | None
   :param s: Lebar feedback dalam bit, kelipatan 8 pada rentang 8..128.
   :type s: int
   :returns: ``IV || C``, panjang ``16 + len(p)``.
   :rtype: bytes
   :raises ValueError: jika ``s`` bukan kelipatan 8 pada 8..128, atau ``iv`` bukan 16 byte.

.. py:function:: decrypt(C: bytes, K: bytes, s: int = 8) -> bytes

   :param C: ``IV || C``.
   :type C: bytes
   :param K: Kunci 16 byte.
   :type K: bytes
   :param s: Lebar feedback, harus sama dengan saat enkripsi.
   :type s: int
   :returns: Plaintext, panjang ``len(C) - 16``.
   :rtype: bytes
   :raises ValueError: jika ``len(C) < 16`` atau ``s`` tidak valid.

OFB
---

.. py:module:: ofb

``O_j = E_K(X_j)``, ``C_j = P_j xor MSB_s(O_j)``, ``X_{j+1} = LSB_{b-s}(X_j) || MSB_s(O_j)``.
Enkripsi dan dekripsi memakai operasi yang sama.

.. py:function:: encrypt(p: bytes, K: bytes, iv: bytes | None = None, s: int = 8) -> bytes

   :param p: Plaintext, panjang bebas.
   :type p: bytes
   :param K: Kunci 16 byte.
   :type K: bytes
   :param iv: IV 16 byte; ``None`` = acak.
   :type iv: bytes | None
   :param s: Lebar feedback dalam bit (kelipatan 8, 8..128).
   :type s: int
   :returns: ``IV || C``.
   :rtype: bytes
   :raises ValueError: jika ``iv`` bukan 16 byte atau ``s`` tidak valid.

.. py:function:: decrypt(C: bytes, K: bytes, s: int = 8) -> bytes

   :param C: ``IV || C``.
   :type C: bytes
   :param K: Kunci 16 byte.
   :type K: bytes
   :param s: Harus sama dengan saat enkripsi.
   :type s: int
   :returns: Plaintext.
   :rtype: bytes
   :raises ValueError: jika ``len(C) < 16`` atau ``s`` tidak valid.

.. py:function:: ofb(data: bytes, K: bytes, iv: bytes, s: int) -> bytes

   Inti OFB: meng-XOR ``data`` dengan keystream. Dipakai bersama oleh ``encrypt`` dan ``decrypt``.

   :param data: Data masukan.
   :type data: bytes
   :param K: Kunci 16 byte.
   :type K: bytes
   :param iv: Nilai awal 16 byte.
   :type iv: bytes
   :param s: Lebar feedback dalam bit.
   :type s: int
   :returns: ``data`` yang dilakukan XOR dengan keystream, panjang sama dengan ``data``.
   :rtype: bytes
   :raises ValueError: jika ``s`` tidak valid.

CTR (Counter)
-------------

.. py:module:: ctr

``C_j = P_j xor E_K(T_j)``, ``T_{j+1} = (T_j + 1) mod 2^128``. Counter 128-bit dibaca big-endian.
Blok terakhir yang pendek di XOR dengan sebagian keystream.

.. py:function:: encrypt(p: bytes, K: bytes, counter: bytes | None = None) -> bytes

   :param p: Plaintext, panjang bebas.
   :type p: bytes
   :param K: Kunci 16 byte.
   :type K: bytes
   :param counter: Nilai awal counter ``T_1``, 16 byte; ``None`` = acak.
   :type counter: bytes | None
   :returns: ``T_1 || C``, panjang ``16 + len(p)``.
   :rtype: bytes
   :raises ValueError: jika ``counter`` bukan 16 byte.

   .. warning::
      Jangan pernah memakai ulang counter awal yang sama dengan kunci yang sama.

.. py:function:: decrypt(C: bytes, K: bytes) -> bytes

   :param C: ``T_1 || C``.
   :type C: bytes
   :param K: Kunci 16 byte.
   :type K: bytes
   :returns: Plaintext, panjang ``len(C) - 16``.
   :rtype: bytes
   :raises ValueError: jika ``len(C) < 16``.

.. py:function:: counter_mode(data: bytes, K: bytes, counter: bytes) -> bytes

   Inti CTR: meng-XOR ``data`` dengan keystream dari counter yang bertambah satu per blok.

   :param data: Data masukan.
   :type data: bytes
   :param K: Kunci 16 byte.
   :type K: bytes
   :param counter: Counter awal 16 byte.
   :type counter: bytes
   :returns: ``data`` yang di XOR dengan keystream.
   :rtype: bytes

Ringkasan format output
-------------------------

.. list-table::
   :header-rows: 1
   :widths: 14 22 30 34

   * - Mode
     - Perlu padding?
     - Format ciphertext
     - Parameter tambahan
   * - ECB
     - Ya (kelipatan 16)
     - ``C``
     - tidak ada
   * - CBC
     - Ya (kelipatan 16)
     - ``IV || C``
     - ``iv``
   * - CFB
     - Tidak
     - ``IV || C``
     - ``iv``, ``s``
   * - OFB
     - Tidak
     - ``IV || C``
     - ``iv``, ``s``
   * - CTR
     - Tidak
     - ``T_1 || C``
     - ``counter``

Notes: :py:func:`soni128.encrypt` tetap menambahkan padding untuk CFB/OFB/CTR sehingga ciphertext
dari API high level selalu 16 + kelipatan 16 byte.
