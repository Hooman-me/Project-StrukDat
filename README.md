# Proyek 2EZ4U Food Delivery

Studi Kasus Proyek Akhir  
Mata Kuliah: Struktur Data dan Analisa Algoritma (EC234303)  
Departemen Teknik Komputer, Fakultas Teknologi Elektro dan Informatika Cerdas  
Institut Teknologi Sepuluh Nopember  

---

## 1. Deskripsi Proyek

2EZ4U Food Delivery adalah implementasi backend engine mini untuk layanan pesan-antar makanan dan barang dengan trafik transaksi tinggi. Proyek ini memodelkan sistem pemrosesan pesanan mulai dari penyimpanan data dalam memori, antrean layanan kurir, penghitungan struk kasir, hingga pengurutan laporan harian dan pencarian data transaksi secara efisien.

Seluruh struktur data dan algoritma inti pada proyek ini dibangun secara mandiri tanpa menggunakan pustaka instan bawaan bahasa pemrograman, seperti struktur kamus (dictionary/set), fungsi pengurutan siap pakai (sorted/.sort()), pustaka heap (heapq), maupun modul pencarian siap pakai (bisect).

Progres pengerjaan sistem pada laporan ini mencakup Milestone 1 (M1) hingga Milestone 3 (M3).

---

## 2. Struktur Berkas dan Direktori

Berikut adalah susunan berkas dalam repositori proyek beserta perannya masing-masing:

```text
StrukDat/
|-- app.py                  Titik masuk utama aplikasi antarmuka grafis (Tkinter)
|-- run.bat                 Skrip peluncur otomatis untuk lingkungan sistem operasi Windows
|-- README.md               Dokumentasi teknis, struktur proyek, dan laporan hasil pengujian
|
|-- data/                   Direktori basis data mentah
|   |-- pesanan.csv         Data transaksi utama sebanyak 200.000 baris pesanan
|   |-- peta.csv            Data keterhubungan lokasi dan estimasi jarak antar titik
|
|-- backend/                Implementasi logika bisnis, struktur data, dan algoritma
|   |-- models.py           Definisi kelas Pesanan dan representasi data entitas
|   |-- m1_pesanan.py       Milestone 1: Struktur data Larik Dinamis (Array) dan Senarai Berantai (LinkList)
|   |-- m2_antrean.py       Milestone 2: Tumpukan (Stack), Antrean (Queue), Mesin Kasir Postfix, dan Undo/Redo
|   |-- m3_laporan.py       Milestone 3: Algoritma Pengurutan (Insertion & Merge Sort) dan Pencarian (Linear & Binary Search)
|
|-- frontend/               Lapisan antarmuka pengguna
|   |-- ui.py               Antarmuka desktop Tkinter dengan panel menu, formulir dinamis, dan pencatat waktu eksekusi
|
|-- test/                   Pengujian mandiri dan tolok ukur performa
    |-- coba_M1.py          Unit test untuk verifikasi fungsionalitas M1
    |-- bench_m1.py         Skrip uji tolok ukur (benchmark) perbandingan operasi M1
```

### Penjelasan Fungsi Tiap Berkas:

1. app.py  
   Berkas inisialisasi utama aplikasi desktop. Bertanggung jawab mengatur jalur impor modul, membuat jendela utama Tkinter, dan menjalankan loop aplikasi.

2. run.bat  
   Skrip otomasi untuk menjalankan aplikasi di Windows. Skrip ini secara otomatis mendeteksi lingkungan Python yang tersedia (baik Python bawaan sistem, MSYS2, maupun Python Launcher) dan memastikan direktori kerja berada di folder proyek sebelum mengeksekusi aplikasi.

3. backend/models.py  
   Menyediakan kelas Pesanan yang merepresentasikan satu baris data pesanan dengan atribut pengenal (oid), nama pelanggan, nama restoran, menu pesanan, nominal harga, tingkat prioritas, stempel waktu masuk, stempel waktu selesai, dan status pesanan. Berkas ini juga memvalidasi tipe data angka dan menyediakan format tampilan yang rapi.

4. backend/m1_pesanan.py  
   Mengimplementasikan dua struktur data dasar: Array (larik dinamis dengan strategi penggandaan kapasitas saat penuh) dan LinkList (senarai berantai tunggal dengan penunjuk simpul kepala dan ekor). Dilengkapi fungsi pembantu seperti pembaca berkas CSV, penambah pesanan sesuai skala prioritas, dan pengukur waktu eksekusi presisi.

5. backend/m2_antrean.py  
   Mengimplementasikan struktur Tumpukan (Stack) dengan prinsip LIFO dan dua jenis Antrean (Queue) dengan prinsip FIFO, yaitu Antrean Naif berbasis larik biasa dan Antrean Melingkar (Circular Queue) berbasis penunjuk berputar. Berkas ini juga mencakup modul mesin kasir untuk konversi infix ke postfix dan evaluasi ekspresi aritmatika, serta mekanisme pembatalan aksi (undo) dan pengerjaan ulang aksi (redo).

6. backend/m3_laporan.py  
   Mengimplementasikan algoritma pengurutan Insertion Sort dan Merge Sort yang stabil, serta algoritma pencarian Linear Search dan Binary Search. Setiap fungsi dirancang untuk melaporkan metrik komputasi nyata berupa jumlah perbandingan kunci dan jumlah pemindahan elemen selain durasi waktu eksekusi.

7. frontend/ui.py  
   Mengatur tampilan visual antarmuka pengguna berbasis Tkinter. Terbagi atas tiga area kerja: daftar navigasi perintah di sebelah kiri, formulir masukan parameter dan tabel penampil hasil di sebelah kanan atas, serta panel COMMAND di sebelah kanan bawah yang mencatat durasi eksekusi dalam satuan milidetik secara langsung.

8. test/coba_M1.py dan test/bench_m1.py  
   Kumpulan skrip pengujian unit dan pengukuran empiris untuk memvalidasi kebenaran logika operasi struktur data dan membandingkan karakteristik komputasi secara langsung pada kumpulan data berukuran masif.

---

## 3. Rincian Milestone

### Milestone 1: Data Pesanan (Array vs LinkList)

Milestone 1 berfokus pada perbandingan karakteristik performa dua struktur data linier fundamental saat melayani 200.000 data transaksi:

Aturan Bisnis Prioritas Pesanan:
- Pesanan VIP (Prioritas 1): Langsung disisipkan di posisi paling depan barisan (indeks 0).
- Pesanan Prioritas (Prioritas 2): Menyerobot masuk tepat ke tengah barisan (indeks n // 2).
- Pesanan Reguler (Prioritas 3): Mengantre secara wajar di barisan paling belakang (append).

Analisis Kompleksitas Teoretis:
- Lihat Pesanan (Akses Indeks ke-i):
  Array membutuhkan waktu O(1) karena lokasi memori dapat dihitung langsung dari alamat pangkal ditambah offset indeks. Sebaliknya, LinkList membutuhkan waktu O(n) karena harus menelusuri rantai simpul satu per satu dari kepala (head).
- Tambah Pesanan Reguler (Ujung Belakang):
  Array mencatatkan waktu O(1) amortized berkat teknik pelipatan kapasitas saat larik penuh. LinkList mencatatkan waktu O(1) mutlak karena memanfaatkan penunjuk ekor (tail).
- Tambah Pesanan Prioritas (Tengah Barisan):
  Array memerlukan O(n) karena harus menggeser separuh elemen di sebelah kanan posisi sisip ke arah kanan. LinkList juga membutuhkan waktu O(n) karena harus menelusuri rantai hingga simpul ke-(n/2) sebelum menyambungkan penunjuk simpul baru.
- Tambah Pesanan VIP (Paling Depan):
  Array membutuhkan waktu O(n) yang signifikan karena seluruh elemen yang ada harus digeser satu langkah ke kanan untuk memberi ruang di indeks 0. Sebaliknya, LinkList mencatatkan waktu O(1) instan karena hanya mengubah tautan simpul kepala baru (prepend).
- Hapus Pesanan:
  Array membutuhkan O(n) untuk menggeser sisa elemen ke arah kiri, sedangkan LinkList membutuhkan O(n) untuk menelusuri simpul target sebelum melepaskan tautannya.

---

### Milestone 2: Tumpukan dan Antrean (Stack & Queue)

Milestone 2 menangani dua kebutuhan operasional utama di kasir dan dapur:

1. Mesin Kasir Postfix (Stack)  
   Struk belanja pelanggan dimasukkan dalam bentuk ekspresi aritmatika manusia (infix), misalnya `( 3 * 12000 ) + ( 2 * 8500 ) - 5000`. Komputer mengevaluasi ekspresi ini melalui dua tahap:
   - Tahap Konversi (Infix ke Postfix): Menggunakan tumpukan operator dengan aturan tingkat kekuatan operator (* dan / lebih tinggi daripada + dan -). Tanda kurung buka didorong ke tumpukan, sedangkan kurung tutup memunculkan operator hingga kurung buka pasangannya ditemukan.
   - Tahap Evaluasi Postfix: Membaca token postfix dari kiri ke kanan menggunakan tumpukan angka. Ketika menemukan operator biner, dua operan teratas diambil dengan urutan yang benar (operan kedua keluar pertama, diikuti operan pertama) untuk menjamin keabsahan operasi non-komutatif seperti pengurangan dan pembagian.

2. Antrean Layanan Kurir (Queue Naif vs Queue Melingkar)  
   Sistem membandingkan dua pendekatan antrean berprinsip FIFO untuk melayani pesanan yang siap diantar:
   - Antrean Naif: Setiap operasi pengambilan pesanan (dequeue) mengambil elemen terdepan pada indeks 0 dan menggeser puluhan ribu sisa elemen satu petak ke kiri. Hal ini menyebabkan kompleksitas O(n) per layanan dan membebani sistem saat antrean panjang.
   - Antrean Melingkar (Circular Queue): Menggunakan sepasang penunjuk (front dan rear) dan pencacah jumlah elemen (count). Operasi dequeue cukup memajukan penunjuk front dengan aritmatika modulo `(front + 1) % kapasitas` tanpa memindahkan satu pun elemen dalam memori, sehingga selalu beroperasi dalam waktu O(1).
   - Keputusan Desain Circular Queue:
     1. Memakai atribut count: Membedakan kondisi penuh (count == cap) dan kosong (count == 0) secara tegas tanpa perlu mengorbankan 1 slot kosong larik.
     2. Antrean tumbuh saat penuh: Saat count mencapai kapasitas (count == cap), kapasitas larik otomatis digandakan 2x lipat (_grow) dan elemen ditata ulang dari indeks 0, sehingga antrean bersifat dinamis tanpa risiko overflow (misal bertumbuh dinamis hingga kapasitas 32.768 pada pemuatan data riil).

3. Mekanisme Pembatalan (Undo dan Redo)  
   Setiap aksi yang mengubah status antrean dicatat ke dalam tumpukan undo terpisah per jenis antrean:
   - ENQUEUE: Pembatalan mengeluarkan kembali pesanan dari belakang kedua antrean.
   - DEQUEUE_NAIF: Pembatalan mengembalikan pesanan ke DEPAN antrean naif saja.
   - DEQUEUE_CIRCULAR: Pembatalan mengembalikan pesanan ke DEPAN antrean circular saja (mencegah duplikasi data pada antrean naif).
   - Efisiensi Pengembalian (kembalikan_ke_depan): Pada antrean naif, seluruh elemen lama digeser sekali jalan ke kanan sejauh k posisi (bukan sekali per elemen). Pada antrean circular, hanya penunjuk front yang dimundurkan modulo tanpa pergeseran elemen memori.
   - Riwayat & Statistik: Tersedia method `history()` yang konsisten dengan urutan `undo_last()`, serta method `stats()` yang merangkum panjang antrean, kapasitas, total geseran, dan kedalaman tumpukan dalam bentuk list of tuple (karena dictionary dilarang).
   - Validasi Mesin Kasir: Memvalidasi dan melempar ValueError pada kasus pembagian nol, operand kurang, kurung tak berpasangan, dua angka berurutan, operator di ujung ekspresi, maupun karakter asing.

---

### Milestone 3: Pengurutan dan Pencarian (Sort & Search)

Milestone 3 menyediakan kemampuan analisis data transaksi untuk penyusunan laporan harian dan pelacakan pesanan:

1. Algoritma Pengurutan:
   - Insertion Sort:
     Mengurutkan data secara in-place dengan cara menyisipkan setiap elemen ke posisi yang tepat pada bagian larik yang sudah terurut di sebelah kirinya. Algoritma ini bersifat stabil (elemen dengan nilai kunci sama tetap mempertahankan urutan kedatangan awalnya) dengan kompleksitas rata-rata O(n^2). Pada antarmuka, pengurutan ini dibatasi maksimal 20.000 data agar tidak membekukan sistem operasi.
   - Merge Sort:
     Menggunakan pendekatan divide-and-conquer dengan membelah kumpulan data hingga berukuran satu elemen, lalu menggabungkannya kembali secara terurut. Penggabungan dilakukan dengan memprioritaskan elemen dari belahan kiri saat nilai kuncinya setara untuk menjamin sifat kestabilan. Kompleksitasnya terjamin O(n log n) pada seluruh kondisi data dan mampu memproses seluruh 200.000 baris pesanan secara cepat.

2. Algoritma Pencarian:
   - Linear Search:
     Memeriksa elemen satu per satu dari indeks pertama hingga menemukan nomor pesanan yang dicari atau hingga akhir larik. Beroperasi dengan kompleksitas O(n) tanpa mensyaratkan data terurut terlebih dahulu.
   - Binary Search:
     Mencari pesanan pada larik yang sudah terurut dengan cara membandingkan target terhadap elemen tengah dan membuang separuh ruang pencarian di setiap langkah. Beroperasi dalam kompleksitas O(log n).

3. Pelaporan Jumlah Perbandingan dan Pemindahan:
   Selain mencatat waktu proses dalam milidetik, setiap fungsi pada M3 melaporkan jumlah operasi perbandingan kunci dan jumlah pemindahan elemen. Metrik ini bersifat deterministik dan membuktikan efisiensi teoritis algoritma terlepas dari spesifikasi perangkat keras komputer yang digunakan.

---

## 4. Cara Menjalankan Aplikasi

### Kebutuhan Sistem:
- Sistem Operasi: Windows 10/11, Linux, atau macOS.
- Interpreter: Python versi 3.11 atau yang lebih baru.
- Pustaka Antarmuka: Modul bawaan Tkinter.

### Langkah Pengoperasian:

1. Menggunakan Skrip Otomatis (Windows):
   Cukup klik ganda pada berkas `run.bat` yang terletak di direktori utama proyek. Jendela terminal akan memverifikasi ketersediaan Python dan membuka antarmuka grafis secara langsung.

2. Menggunakan Baris Perintah (Terminal / PowerShell):
   Buka terminal pada direktori proyek, lalu jalankan perintah berikut:

   ```bash
   python app.py
   ```

3. Alur Penggunaan pada Antarmuka:
   - Langkah Pertama: Klik menu `DATA - Load CSV` pada panel kiri, lalu tekan tombol `MUAT DATA` untuk mengunggah 200.000 data transaksi ke dalam memori.
   - Uji Coba M1: Pilih salah satu menu `ARRAY` atau `LINKEDLIST` untuk mengamati perbedaan waktu saat melihat, menyisipkan (Reguler, Prioritas, VIP), maupun menghapus pesanan.
   - Uji Coba M2: Pilih menu `STACK - POSTFIX` untuk mengevaluasi struk hitung kasir, atau bandingkan `QUEUE - DEQUEUE NAIF` dengan `QUEUE - DEQUEUE CIRCULAR` untuk melihat kontras pergeseran elemen memori. Coba fitur `STACK - UNDO` dan `STACK - REDO` untuk mengamati pembalikan aksi antrean.
   - Uji Coba M3: Jalankan menu `SORT` untuk membandingkan jumlah perbandingan antara Insertion Sort dan Merge Sort, lalu bandingkan kecepatan pencarian pada menu `SEARCH` antara Linear Search dan Binary Search.

---

## 5. Ringkasan Hasil Pengujian dan Benchmark

Berikut adalah ringkasan hasil pengukuran empiris rata-rata yang dilakukan pada data riil 200.000 transaksi pesanan:

### Hasil Benchmark M1 (Posisi Tengah n = 100.000):

| Operasi                         | Karakteristik Array | Karakteristik LinkList | Keterangan Operasi |
|:--------------------------------|:-------------------:|:----------------------:|:-------------------|
| Lihat Pesanan (Akses Indeks)    | 0.003 ms (O(1))     | 1.621 ms (O(n))        | Array unggul mutlak karena pengalamatan langsung |
| Tambah Reguler (Paling Belakang)| 0.002 ms (O(1))     | 0.002 ms (O(1))        | Kedua struktur sama cepat di ujung ekor |
| Tambah Prioritas (Tengah)       | 4.413 ms (O(n))     | 1.689 ms (O(n))        | Array menggeser elemen; LinkList menelusuri rantai |
| Tambah VIP (Paling Depan)       | 12.291 ms (O(n))    | 0.008 ms (O(1))        | LinkList unggul telak karena hanya menyambung head |
| Hapus Pesanan (Tengah)          | 4.905 ms (O(n))     | 1.987 ms (O(n))        | Keduanya O(n) dengan pola beban kerja berbeda |

### Hasil Benchmark M2 (Antrean 19.850 Pesanan Status ANTRE):

| Operasi                         | Antrean Naif        | Antrean Melingkar      | Analisis Perbandingan |
|:--------------------------------|:-------------------:|:----------------------:|:----------------------|
| Dequeue 1 Pesanan               | 1.07 ms (19.850 geser)| 0.01 ms (0 geser)    | Antrean melingkar tidak memindahkan elemen |
| Dequeue 100 Pesanan             | 93.27 ms (1.9 jt geser)| 0.03 ms (0 geser)   | Selisih waktu membuktikan keunggulan O(1) modulo |
| Evaluasi Struk Kasir Postfix    | 0.09 ms             | -                      | Evaluasi stack selesai instan dan akurat |

### Hasil Benchmark M3 (Pengurutan & Pencarian):

| Skenario Operasi                | Algoritma / Metode  | Metrik Operasi         | Waktu Eksekusi |
|:--------------------------------|:-------------------:|:----------------------:|:---------------|
| Urutkan 2.000 Data (Kunci Harga)| Insertion Sort      | 962.430 perbandingan   | 163.26 ms      |
| Urutkan 2.000 Data (Kunci Harga)| Merge Sort          | 19.240 perbandingan    | 6.36 ms        |
| Urutkan 4.000 Data (Kunci Harga)| Insertion Sort      | 3.831.520 perbandingan | 660.36 ms (tumbuh 4x) |
| Urutkan 4.000 Data (Kunci Harga)| Merge Sort          | 42.355 perbandingan    | 13.66 ms (tumbuh 2x) |
| Urutkan 200.000 Data Penuh      | Merge Sort          | 3.226.139 perbandingan | 1.13 detik     |
| Cari ID Pesanan (Indeks 199.998)| Linear Search       | 199.999 perbandingan   | 24.52 ms       |
| Cari ID Pesanan (Indeks 199.998)| Binary Search       | 17 perbandingan        | 0.03 ms        |

---

## 6. Catatan Pengujian Unit

Seluruh modul pengujian unit dapat dijalankan melalui berkas uji di dalam direktori `test/` untuk memastikan integritas kode tetap terjaga sebelum demonstrasi proyek dilakukan:

```bash
python test/coba_M1.py
```
Semua tes telah melewati pengujian dengan status lulus tanpa kesalahan.
