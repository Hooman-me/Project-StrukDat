# test/coba_M3.py

import sys
import os
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.m3_laporan import (
    insertion_sort, merge_sort, linear_search, binary_search
)
from backend.models import Pesanan


class TestM3SortSearch(unittest.TestCase):

    def test_kestabilan_pengurutan(self):
        # Menguji kestabilan: dua elemen berharga sama harus tetap mempertahankan urutan aslinya
        p1 = Pesanan("O-001", "A", "resto-a", "m1", 15000, 3, 10, None, "ANTRE")
        p2 = Pesanan("O-002", "B", "resto-b", "m2", 10000, 3, 20, None, "ANTRE")
        p3 = Pesanan("O-003", "C", "resto-c", "m3", 10000, 3, 30, None, "ANTRE")
        p4 = Pesanan("O-004", "D", "resto-d", "m4", 25000, 3, 40, None, "ANTRE")

        data = [p1, p2, p3, p4]

        # Insertion sort
        hasil_is, cmp_is, mov_is = insertion_sort(list(data), "harga")
        self.assertEqual(hasil_is[0].oid, "O-002")
        self.assertEqual(hasil_is[1].oid, "O-003") # O-002 tetap sebelum O-003

        # Merge sort
        hasil_ms, cmp_ms, mov_ms = merge_sort(list(data), "harga")
        self.assertEqual(hasil_ms[0].oid, "O-002")
        self.assertEqual(hasil_ms[1].oid, "O-003")

    def test_insertion_sort_batas_maksimal(self):
        data_besar = [i for i in range(25000)]
        with self.assertRaises(ValueError):
            insertion_sort(data_besar, batas_maks=20000)

    def test_binary_search_empat_kasus_dan_kosong(self):
        # 1. Larik kosong
        idx, _ = binary_search([], "O-001")
        self.assertEqual(idx, -1)

        larik = ["O-001", "O-003", "O-005", "O-007", "O-009"]

        # 2. Target di tengah
        idx, _ = binary_search(larik, "O-005")
        self.assertEqual(idx, 2)

        # 3. Target di kiri
        idx, _ = binary_search(larik, "O-001")
        self.assertEqual(idx, 0)

        # 4. Target di kanan
        idx, _ = binary_search(larik, "O-009")
        self.assertEqual(idx, 4)

        # 5. Target tidak ada
        idx, _ = binary_search(larik, "O-004")
        self.assertEqual(idx, -1)

    def test_linear_search(self):
        larik = ["O-010", "O-005", "O-020", "O-001"]
        idx, cmp_cnt = linear_search(larik, "O-020")
        self.assertEqual(idx, 2)
        self.assertEqual(cmp_cnt, 3)

        idx_gagal, cmp_gagal = linear_search(larik, "O-999")
        self.assertEqual(idx_gagal, -1)
        self.assertEqual(cmp_gagal, 4)


if __name__ == "__main__":
    unittest.main()
