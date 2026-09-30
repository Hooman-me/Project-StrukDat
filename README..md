TESTING


Percobaan Pertama: 
--- 1. LIHAT PESANAN KE-100000 ---
  Array      : 0.0033 ms  (Teori O(1))
  LinkList   : 1.4585 ms  (Teori O(n))

--- 2. TAMBAH PESANAN REGULER (BELAKANG) ---
  Array      : 0.0024 ms  (Teori O(1) amortized)
  LinkList   : 0.0260 ms  (Teori O(1) tail)

--- 3. TAMBAH PESANAN PRIORITAS (TENGAH) ---
  Array      : 4.8578 ms  (Teori O(n) geser separuh elemen)
  LinkList   : 1.7825 ms  (Teori O(n) telusur separuh rantai)

--- 4. TAMBAH PESANAN VIP (PALING DEPAN) ---
  Array      : 10.8761 ms  (Teori O(n) geser seluruh elemen)
  LinkList   : 0.0069 ms  (Teori O(1) ubah head)

--- 5. HAPUS PESANAN KE-100000 ---
  Array      : 4.9052 ms  (Teori O(n) geser kiri)
  LinkList   : 1.9878 ms  (Teori O(n) telusur ke i-1)

========================================================
Ringkasan Hasil Benchmark (ms):
Operasi              | Array        | LinkList    
--------------------------------------------------
Lihat Pesanan        |   0.0033 ms |   1.4585 ms
Tambah REGULER       |   0.0024 ms |   0.0260 ms
Tambah PRIORITAS     |   4.8578 ms |   1.7825 ms
Tambah VIP           |  10.8761 ms |   0.0069 ms
Hapus Pesanan        |   4.9052 ms |   1.9878 ms
========================================================

Percobaan Kedua:
--- 1. LIHAT PESANAN KE-100000 ---
  Array      : 0.0036 ms  (Teori O(1))
  LinkList   : 1.6211 ms  (Teori O(n))

--- 2. TAMBAH PESANAN REGULER (BELAKANG) ---
  Array      : 0.0022 ms  (Teori O(1) amortized)
  LinkList   : 0.0021 ms  (Teori O(1) tail)

--- 3. TAMBAH PESANAN PRIORITAS (TENGAH) ---
  Array      : 4.4133 ms  (Teori O(n) geser separuh elemen)
  LinkList   : 1.6891 ms  (Teori O(n) telusur separuh rantai)

--- 4. TAMBAH PESANAN VIP (PALING DEPAN) ---
  Array      : 14.0635 ms  (Teori O(n) geser seluruh elemen)
  LinkList   : 0.0087 ms  (Teori O(1) ubah head)

--- 5. HAPUS PESANAN KE-100000 ---
  Array      : 4.5923 ms  (Teori O(n) geser kiri)
  LinkList   : 1.6383 ms  (Teori O(n) telusur ke i-1)

========================================================
Ringkasan Hasil Benchmark (ms):
Operasi              | Array        | LinkList    
--------------------------------------------------
Lihat Pesanan        |   0.0036 ms |   1.6211 ms
Tambah REGULER       |   0.0022 ms |   0.0021 ms
Tambah PRIORITAS     |   4.4133 ms |   1.6891 ms
Tambah VIP           |  14.0635 ms |   0.0087 ms
Hapus Pesanan        |   4.5923 ms |   1.6383 ms
========================================================

Percobaan Ketiga: 
--- 1. LIHAT PESANAN KE-100000 ---
  Array      : 0.0026 ms  (Teori O(1))
  LinkList   : 1.7771 ms  (Teori O(n))

--- 2. TAMBAH PESANAN REGULER (BELAKANG) ---
  Array      : 0.0020 ms  (Teori O(1) amortized)
  LinkList   : 0.0018 ms  (Teori O(1) tail)

--- 3. TAMBAH PESANAN PRIORITAS (TENGAH) ---
  Array      : 4.3729 ms  (Teori O(n) geser separuh elemen)
  LinkList   : 1.6109 ms  (Teori O(n) telusur separuh rantai)

--- 4. TAMBAH PESANAN VIP (PALING DEPAN) ---
  Array      : 12.2919 ms  (Teori O(n) geser seluruh elemen)
  LinkList   : 0.0079 ms  (Teori O(1) ubah head)

--- 5. HAPUS PESANAN KE-100000 ---
  Array      : 5.5902 ms  (Teori O(n) geser kiri)
  LinkList   : 3.1877 ms  (Teori O(n) telusur ke i-1)

========================================================
Ringkasan Hasil Benchmark (ms):
Operasi              | Array        | LinkList    
--------------------------------------------------
Lihat Pesanan        |   0.0026 ms |   1.7771 ms
Tambah REGULER       |   0.0020 ms |   0.0018 ms
Tambah PRIORITAS     |   4.3729 ms |   1.6109 ms
Tambah VIP           |  12.2919 ms |   0.0079 ms
Hapus Pesanan        |   5.5902 ms |   3.1877 ms
========================================================