# backend/m3_laporan.py

def _nilai(x, kunci):
    if kunci is None:
        return x
    return kunci(x)


def insertion_sort(larik, kunci=None):
    n = len(larik)
    for i in range(1, n):
        sisip = larik[i]                  # kartu yang mau disisipkan
        k_sisip = _nilai(sisip, kunci)
        j = i - 1                         # mulai bandingkan dari kiri-nya
        while j >= 0 and _nilai(larik[j], kunci) > k_sisip:
            larik[j + 1] = larik[j]       # geser ke kanan 1 langkah
            j -= 1
        larik[j + 1] = sisip              # taruh di celah yang tersisa
    return larik


def binary_search(larik, target, kunci=None):
    kiri = 0
    kanan = len(larik) - 1
    while kiri <= kanan:
        tengah = (kiri + kanan) // 2
        nilai = _nilai(larik[tengah], kunci)
        if nilai == target:
            return tengah                 # ketemu: kembalikan indeksnya
        elif nilai < target:
            kiri = tengah + 1             # target ada di sebelah kanan
        else:
            kanan = tengah - 1            # target ada di sebelah kiri
    return -1                             # tidak ketemu