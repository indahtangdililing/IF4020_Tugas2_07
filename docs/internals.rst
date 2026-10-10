Komponen internal
=================

Modul-modul yang kami jelaskan berikut dipanggil oleh :doc:`cipher`. Biasanya tidak perlu dipanggil langsung,
tetapi dibutuhkan untuk menguji rancangan cipher.

Penjadwalan kunci (``key_schedule``)
------------------------------------

.. py:module:: key_schedule

.. py:function:: key_schedule(key: bytes, R: int) -> tuple[list[int], list[int], list[int]]

   Menurunkan seluruh *subkey* dari kunci 16 byte. Delapan output pertama dari
   :py:func:`key_stream` dibuang, lalu sisanya dipakai berurutan.

   :param key: Kunci master, tepat 16 byte.
   :type key: bytes
   :param R: Jumlah ronde, minimal 4.
   :type R: int
   :returns: Tuple ``(wk, rk, mk)``:

      * ``wk``: 8 word *whitening* (4 awal untuk input, 4 akhir untuk output).
      * ``rk``: ``2 * R`` *round key*, dua per ronde.
      * ``mk``: 4 word untuk setiap *mixing layer* (8 *word* bila ``R = 18``).
   :rtype: tuple[list[int], list[int], list[int]]
   :raises AssertionError: jika ``len(key) != 16`` atau ``R < 4``.

.. py:function:: key_stream(key: bytes) -> Iterator[int]

   Generator tak hingga yang menghasilkan word 32-bit. Kunci dibaca sebagai empat word
   ``k, l0, l1, l2``; setiap langkah menghitung ``x = ((rotr(l0, 8) + k) mod 2^32) xor i``,
   ``k = rotl(k, 3) xor x``, menggeser ``(l0, l1, l2) = (l1, l2, x)``, lalu mengeluarkan ``k``.

   :param key: Kunci 16 byte.
   :type key: bytes
   :returns: *Generator* bilangan bulat 32-bit.
   :rtype: Iterator[int]

.. py:function:: is_ml(r: int, R: int) -> bool

   Menentukan apakah mixing layer dijalankan setelah ronde ke-``r`` (mulai dari 0).

   :param r: Indeks ronde.
   :type r: int
   :param R: Jumlah ronde total.
   :type R: int
   :returns: ``True`` jika ``(r + 1) % 6 == 0`` dan ``r != R - 1``.
   :rtype: bool

.. py:function:: rotl(x: int, n: int) -> int
                 rotr(x: int, n: int) -> int

   Rotasi bit ke kiri/kanan pada word 32-bit.

   :param x: Nilai 32-bit.
   :type x: int
   :param n: Jumlah bit rotasi (0 < n < 32).
   :type n: int
   :returns: Hasil rotasi, 32-bit.
   :rtype: int

Fungsi Feistel ``F`` (``f``)
----------------------------

.. py:module:: f

.. py:data:: SBOX
   :type: list[int]

   S-box 4-bit (16 entri): ``[5, 12, 15, 2, 0, 9, 3, 4, 10, 7, 6, 1, 13, 14, 8, 11]``.

.. py:function:: F(x: int, rk: int) -> int

   ``F(x, rk) = ROT(substitution((x xor rk) & 0xFFFFFFFF))``.

   :param x: *Word* masukan 32-bit.
   :type x: int
   :param rk: *Round key* 32-bit.
   :type rk: int
   :returns: *Word* 32-bit.
   :rtype: int

.. py:function:: substitution(x: int) -> int

   Mengganti setiap dari 8 nibble pada ``x`` melalui :py:data:`SBOX`.

   :param x: Nilai 32-bit.
   :type x: int
   :returns: Nilai 32-bit hasil substitusi.
   :rtype: int

.. py:function:: ROT(t: int) -> int

   Difusi linear: ``t xor rotl32(t, 4) xor rotl32(t, 8) xor rotl32(t, 12)``.

   :param t: Nilai 32-bit.
   :type t: int
   :returns: Nilai 32-bit.
   :rtype: int

.. py:function:: rotl32(x: int, n: int) -> int

   Rotasi kiri 32-bit (``n`` diambil modulo 32).

   :param x: Nilai 32-bit.
   :type x: int
   :param n: Jumlah bit.
   :type n: int
   :returns: Hasil rotasi.
   :rtype: int

Mixing layer (``mixing_layer``)
-------------------------------

.. py:module:: mixing_layer

.. py:function:: ML(x0: int, x1: int, x2: int, x3: int, mk: Sequence[int], mk2: Sequence[int] | None = None) -> tuple[int, int, int, int]

   Melakukan XOR keempat word dengan ``mk``, memecahnya menjadi delapan setengah word 16-bit
   ``b1..b8``, menerapkan rangkaian operasi tambah/XOR/rotasi 16-bit, lalu menyusun ulang
   menjadi empat word 32-bit.

   :param x0: Word 32-bit ke-0.
   :type x0: int
   :param x1: Word 32-bit ke-1.
   :type x1: int
   :param x2: Word 32-bit ke-2.
   :type x2: int
   :param x3: Word 32-bit ke-3.
   :type x3: int
   :param mk: Empat word kunci ``K1..K4``.
   :type mk: Sequence[int]
   :param mk2: Opsional, empat word untuk output whitening. Tidak dipakai oleh ``cipher``.
   :type mk2: Sequence[int] | None
   :returns: Empat word 32-bit.
   :rtype: tuple[int, int, int, int]

.. py:function:: ML_inv(y0: int, y1: int, y2: int, y3: int, mk: Sequence[int], mk2: Sequence[int] | None = None) -> tuple[int, int, int, int]

   Kebalikan :py:func:`ML`; ``ML_inv(*ML(*x, mk), mk) == x``.

   :param y0: Word 32-bit ke-0.
   :type y0: int
   :param y1: Word 32-bit ke-1.
   :type y1: int
   :param y2: Word 32-bit ke-2.
   :type y2: int
   :param y3: Word 32-bit ke-3.
   :type y3: int
   :param mk: Word kunci yang sama dengan saat ``ML``.
   :type mk: Sequence[int]
   :param mk2: Opsional, sama dengan ``ML``.
   :type mk2: Sequence[int] | None
   :returns: Empat word 32-bit.
   :rtype: tuple[int, int, int, int]

Permutasi ronde (``rp``)
------------------------

.. py:module:: rp

.. py:function:: RP(x0: int, x1: int, x2: int, x3: int) -> tuple[int, int, int, int]

   Permutasi urutan word: ``(x0, x1, x2, x3) -> (x3, x0, x1, x2)``.

   :param x0: Word 32-bit ke-0.
   :type x0: int
   :param x1: Word 32-bit ke-1.
   :type x1: int
   :param x2: Word 32-bit ke-2.
   :type x2: int
   :param x3: Word 32-bit ke-3.
   :type x3: int
   :returns: Empat word yang sudah diputar.
   :rtype: tuple[int, int, int, int]

.. py:function:: RP_inv(x0: int, x1: int, x2: int, x3: int) -> tuple[int, int, int, int]

   Kebalikan :py:func:`RP`: ``(x0, x1, x2, x3) -> (x1, x2, x3, x0)``.

   :param x0: Word 32-bit ke-0.
   :type x0: int
   :param x1: Word 32-bit ke-1.
   :type x1: int
   :param x2: Word 32-bit ke-2.
   :type x2: int
   :param x3: Word 32-bit ke-3.
   :type x3: int
   :returns: Empat word dalam urutan semula.
   :rtype: tuple[int, int, int, int]
