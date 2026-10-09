Modul ``cipher`` (satu blok)
============================

.. py:module:: cipher

Enkripsi dan dekripsi **satu blok 16 byte**. Modul ini adalah inti SONI128, seluruh mode operasi
memanggil fungsi di sini.

.. py:data:: ROUNDS
   :type: int
   :value: 18

   Jumlah ronde bawaan.

.. py:function:: encrypt_block(block: bytes, key: bytes, R: int = 18) -> bytes

   Mengenkripsi satu blok.

   :param block: Plaintext, tepat 16 byte.
   :type block: bytes
   :param key: Kunci, tepat 16 byte.
   :type key: bytes
   :param R: Jumlah ronde, minimal 4. Dekripsi harus memakai nilai yang sama.
   :type R: int
   :returns: Ciphertext 16 byte.
   :rtype: bytes
   :raises AssertionError: jika ``len(block) != 16``, ``len(key) != 16``, atau ``R < 4``.

.. py:function:: decrypt_block(block: bytes, key: bytes, R: int = 18) -> bytes

   Kebalikan dari :py:func:`encrypt_block`.

   :param block: Ciphertext, tepat 16 byte.
   :type block: bytes
   :param key: Kunci, tepat 16 byte.
   :type key: bytes
   :param R: Jumlah ronde, harus sama dengan saat enkripsi.
   :type R: int
   :returns: Plaintext 16 byte.
   :rtype: bytes
   :raises AssertionError: jika ``len(block) != 16``, ``len(key) != 16``, atau ``R < 4``.

.. py:function:: to_words(b: bytes) -> list[int]

   Memecah 16 byte menjadi 4 *word* 32-bit *big-endian*.

   :param b: Data 16 byte.
   :type b: bytes
   :returns: Empat bilangan bulat 0..2\ :sup:`32`-1.
   :rtype: list[int]

.. py:function:: to_bytes(w: Iterable[int]) -> bytes

   Kebalikan :py:func:`to_words`.

   :param w: Empat *word* 32-bit.
   :type w: Iterable[int]
   :returns: 16 byte *big-endian*.
   :rtype: bytes

Alur enkripsi satu blok
-----------------------

.. code-block:: text

   x0..x3 = words(block) xor wk[0..3]                 # input whitening
   for r in 0 .. R-1:
       x1 ^= F(x0, rk[2r])                            # cabang Feistel 1
       x3 ^= F(x2, rk[2r+1])                          # cabang Feistel 2
       (x0,x1,x2,x3) = RP(x0,x1,x2,x3)                # permutasi: (x3,x0,x1,x2)
       if (r+1) % 6 == 0 and r != R-1:                # setelah ronde 6 dan 12 (R=18)
           (x0,x1,x2,x3) = ML(x0,x1,x2,x3, mk[4 word berikutnya])
   ciphertext = bytes(x xor wk[4..7])                 # output whitening

Dekripsi menjalankan langkah yang sama secara terbalik, memakai ``RP_inv`` dan ``ML_inv``.
