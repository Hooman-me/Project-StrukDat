# backend/m3_laporan.py

import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)


def _nilai(x, kunci):
    """Mengekstrak nilai kunci dari suatu objek atau item."""
    if kunci is None:
        return x
    if callable(kunci):
        return kunci(x)
    if isinstance(kunci, str):
        if kunci == "oid":
            return getattr(x, "oid", str(x))
        elif kunci == "harga":
            return getattr(x, "harga", 0)
        elif kunci == "selesai" or kunci == "t_selesai_detik":
            v = getattr(x, "t_selesai_detik", None)
            return v if v is not None else 999999999
        elif kunci == "masuk" or kunci == "t_masuk_detik":
            return getattr(x, "t_masuk_detik", 0)
        elif kunci == "prioritas":
            return getattr(x, "prioritas", 3)
        elif kunci == "pelanggan":
            return getattr(x, "pelanggan", "")
        return getattr(x, kunci, x)
    return x


# ---------------------------------------------------------------------------
# Algoritma Pengurutan (Sorting)
# ---------------------------------------------------------------------------

def insertion_sort(larik, kunci=None, batas_maks=20000):
    """Algoritma Insertion Sort: in-place dan stabil.
    
    Menghitung jumlah perbandingan dan jumlah pemindahan elemen.
    Bila data melebihi batas_maks, raise ValueError agar tidak membekukan sistem.
    Mengembalikan tuple: (larik, perbandingan, pemindahan)
    """
    n = len(larik)
    if n > batas_maks:
        raise ValueError(f"DITOLAK: batasnya {batas_maks:,} baris, pakai merge sort untuk data penuh.")

    perbandingan = 0
    pemindahan = 0

    for i in range(1, n):
        sisip = larik[i]
        k_sisip = _nilai(sisip, kunci)
        j = i - 1
        
        # Perbandingan stabil: hanya geser bila elemen kiri LEBIH BESAR ( > )
        while j >= 0:
            perbandingan += 1
            if _nilai(larik[j], kunci) > k_sisip:
                larik[j + 1] = larik[j]
                pemindahan += 1
                j -= 1
            else:
                break
                
        larik[j + 1] = sisip
        pemindahan += 1

    return (larik, perbandingan, pemindahan)


def merge_sort(larik, kunci=None):
    """Algoritma Merge Sort: membelah lalu menggabungkan secara stabil.
    
    Menghitung jumlah perbandingan dan pemindahan elemen.
    Mampu mengurutkan skala besar hingga 200.000 baris.
    Mengembalikan tuple: (larik_terurut, perbandingan, pemindahan)
    """
    n = len(larik)
    if n <= 1:
        return (larik, 0, 0)

    stats = [0, 0]  # [perbandingan, pemindahan]

    def _ms(arr):
        panjang = len(arr)
        if panjang <= 1:
            return arr

        tengah = panjang // 2
        kiri = _ms(arr[:tengah])
        kanan = _ms(arr[tengah:])

        hasil = []
        i = 0
        j = 0
        len_kiri = len(kiri)
        len_kanan = len(kanan)

        while i < len_kiri and j < len_kanan:
            stats[0] += 1
            # Syarat perbandingan stabil: pakai <= agar elemen kiri didahulukan
            if _nilai(kiri[i], kunci) <= _nilai(kanan[j], kunci):
                hasil.append(kiri[i])
                stats[1] += 1
                i += 1
            else:
                hasil.append(kanan[j])
                stats[1] += 1
                j += 1

        while i < len_kiri:
            hasil.append(kiri[i])
            stats[1] += 1
            i += 1

        while j < len_kanan:
            hasil.append(kanan[j])
            stats[1] += 1
            j += 1

        return hasil

    terurut = _ms(larik)
    return (terurut, stats[0], stats[1])


# ---------------------------------------------------------------------------
# Algoritma Pencarian (Searching)
# ---------------------------------------------------------------------------

def linear_search(larik, target, kunci="oid"):
    """Algoritma Linear Search: memeriksa elemen satu per satu dari depan.
    
    Tidak menuntut data terurut.
    Mengembalikan tuple: (indeks, perbandingan)
    Indeks bernilai -1 jika target tidak ditemukan.
    """
    perbandingan = 0
    target_str = str(target).strip()

    for idx in range(len(larik)):
        perbandingan += 1
        val = str(_nilai(larik[idx], kunci)).strip()
        if val == target_str:
            return (idx, perbandingan)

    return (-1, perbandingan)


def binary_search(larik, target, kunci="oid"):
    if kunci in ("harga", "prioritas", "masuk", "t_masuk_detik", "selesai", "t_selesai_detik"):
        target = int(target)            # kunci angka dibandingkan sebagai angka
    else:
        target = str(target).strip()    # kunci teks dibandingkan sebagai teks
    kiri, kanan, perbandingan = 0, len(larik) - 1, 0
    while kiri <= kanan:
        tengah = (kiri + kanan) // 2
        perbandingan += 1
        val = _nilai(larik[tengah], kunci)
        if isinstance(target, str):
            val = str(val).strip()
        if val == target:
            return (tengah, perbandingan)
        elif val < target:
            kiri = tengah + 1
        else:
            kanan = tengah - 1
    return (-1, perbandingan)