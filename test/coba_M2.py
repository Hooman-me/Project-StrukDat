# test/coba_M2.py

import sys
import os
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.m2_antrean import (
    Stack, AntreanNaif, AntreanMelingkar, PengelolaAntrean,
    ke_postfix, hitung
)
from backend.models import Pesanan


class TestM2StackQueue(unittest.TestCase):

    def test_stack_dasar(self):
        s = Stack(cap=4)
        self.assertTrue(s.is_empty())
        s.push(10)
        s.push(20)
        s.push(30)
        self.assertEqual(len(s), 3)
        self.assertEqual(s.peek(), 30)
        self.assertEqual(s.pop(), 30)
        self.assertEqual(s.pop(), 20)
        self.assertEqual(s.pop(), 10)
        self.assertIsNone(s.pop())

    def test_mesin_kasir_postfix(self):
        # Ekspresi acuan dari modul proyek
        ekspresi = "( 3 * 12000 ) + ( 2 * 8500 ) - 5000"
        tokens, str_post, langkah = ke_postfix(ekspresi)
        self.assertEqual(str_post, "3 12000 * 2 8500 * + 5000 -")
        
        total, langkah_eval = hitung(tokens)
        self.assertEqual(total, 48000)

    def test_antrean_melingkar_berputar(self):
        # Uji kapasitas kecil K = 4 sesuai saran di dokumen proyek
        q = AntreanMelingkar(cap=4)
        q.enqueue("A")
        q.enqueue("B")
        q.enqueue("C")
        self.assertEqual(q.dequeue(), "A")
        self.assertEqual(q.dequeue(), "B")
        q.enqueue("D")
        q.enqueue("E")
        q.enqueue("F")
        self.assertEqual(q.dequeue(), "C")
        self.assertEqual(q.dequeue(), "D")
        self.assertEqual(q.dequeue(), "E")
        self.assertEqual(q.dequeue(), "F")
        self.assertTrue(q.is_empty())

    def test_antrean_naif_geseran(self):
        q = AntreanNaif(cap=4)
        q.enqueue("A")
        q.enqueue("B")
        q.enqueue("C")
        el = q.dequeue()
        self.assertEqual(el, "A")
        self.assertEqual(q.geseran_terakhir, 2)

    def test_undo_redo_enqueue_dequeue(self):
        mgr = PengelolaAntrean()
        p1 = Pesanan("O-1", "Budi", "resto-a", "burger", 20000, 3, 100, None, "ANTRE")
        p2 = Pesanan("O-2", "Siti", "resto-b", "pizza", 45000, 1, 105, None, "ANTRE")

        mgr.enqueue(p1)
        mgr.enqueue(p2)
        self.assertEqual(len(mgr.circular), 2)

        # Undo enqueue p2
        hasil = mgr.undo_last()
        self.assertEqual(hasil[0], "ENQUEUE")
        self.assertEqual(len(mgr.circular), 1)

        # Redo enqueue p2
        hasil = mgr.redo_last()
        self.assertEqual(hasil[0], "ENQUEUE")
        self.assertEqual(len(mgr.circular), 2)

    def test_undo_redo_per_antrean(self):
        mgr = PengelolaAntrean()
        p1 = Pesanan("O-1", "Budi", "resto-a", "burger", 20000, 3, 100, None, "ANTRE")
        p2 = Pesanan("O-2", "Siti", "resto-b", "pizza", 45000, 1, 105, None, "ANTRE")
        mgr.enqueue(p1)
        mgr.enqueue(p2)

        # Dequeue circular 1 kali
        res_circ = mgr.dequeue_circular(1)
        self.assertEqual(len(res_circ), 1)
        self.assertEqual(len(mgr.circular), 1)
        self.assertEqual(len(mgr.naif), 2)  # Antrean naif tidak berkurang

        # Undo dequeue circular
        hasil = mgr.undo_last()
        self.assertEqual(hasil[0], "DEQUEUE_CIRCULAR")
        self.assertEqual(len(mgr.circular), 2)
        self.assertEqual(len(mgr.naif), 2)  # Naif tetap 2, tidak duplikasi

        # Dequeue naif 1 kali
        res_naif = mgr.dequeue_naif(1)
        self.assertEqual(len(res_naif), 1)
        self.assertEqual(len(mgr.naif), 1)
        self.assertEqual(len(mgr.circular), 2)  # Circular tidak berkurang

        # Undo dequeue naif
        hasil = mgr.undo_last()
        self.assertEqual(hasil[0], "DEQUEUE_NAIF")
        self.assertEqual(len(mgr.naif), 2)
        self.assertEqual(len(mgr.circular), 2)

    def test_history_dan_stats(self):
        mgr = PengelolaAntrean()
        p1 = Pesanan("O-1", "Budi", "resto-a", "burger", 20000, 3, 100, None, "ANTRE")
        mgr.enqueue(p1)

        # History harus konsisten dengan aksi
        hist = mgr.history()
        self.assertEqual(len(hist), 1)
        self.assertEqual(hist[0][0], "ENQUEUE")

        # Stats harus list of tuple dan bukan dict
        st = mgr.stats()
        self.assertIsInstance(st, list)
        self.assertNotIsInstance(st, dict)
        stat_dict = dict(st)
        self.assertEqual(stat_dict["panjang_naif"], 1)
        self.assertEqual(stat_dict["panjang_circular"], 1)
        self.assertEqual(stat_dict["undo_depth"], 1)
        self.assertEqual(stat_dict["redo_depth"], 0)

    def test_validasi_mesin_kasir(self):
        # 1. Pembagian nol
        with self.assertRaises(ValueError):
            hitung(ke_postfix("10 / 0")[0])

        # 2. Operator di ujung
        with self.assertRaises(ValueError):
            ke_postfix("+ 5 * 2")
        with self.assertRaises(ValueError):
            ke_postfix("5 * 2 +")

        # 3. Operand kurang
        with self.assertRaises(ValueError):
            hitung(["5", "+"])

        # 4. Kurung tak berpasangan
        with self.assertRaises(ValueError):
            ke_postfix("( 3 * 2")
        with self.assertRaises(ValueError):
            ke_postfix("3 * 2 )")

        # 5. Dua angka berurutan
        with self.assertRaises(ValueError):
            ke_postfix("3 5 + 2")

        # 6. Karakter asing
        with self.assertRaises(ValueError):
            ke_postfix("3 + 2 $ 5")


if __name__ == "__main__":
    unittest.main()
