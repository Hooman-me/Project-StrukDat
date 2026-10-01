# tests/coba_M1.py

import sys
import os
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.m1_pesanan import Array, LinkList
from backend.models import Pesanan


class TestM1StrukturData(unittest.TestCase):

    def test_array_dasar(self):
        arr = Array(initial_capacity=4)
        self.assertEqual(len(arr), 0)
        self.assertEqual(arr.cap, 4)

        # Append memicu resize
        for i in range(1, 6):
            arr.append(f"O-{i:03d}")
        self.assertEqual(len(arr), 5)
        self.assertEqual(arr.cap, 8)
        self.assertEqual(arr.get(0), "O-001")
        self.assertEqual(arr.get(4), "O-005")

        # Insert VIP 
        arr.insert_vip("VIP-001")
        self.assertEqual(len(arr), 6)
        self.assertEqual(arr.get(0), "VIP-001")
        self.assertEqual(arr.get(1), "O-001")

        # Insert Prioritas 
        arr.insert_prioritas("PRIO-001")
        self.assertEqual(len(arr), 7)
        self.assertEqual(arr.get(3), "PRIO-001")

        # Delete
        val_vip = arr.delete(0)
        self.assertEqual(val_vip, "VIP-001")
        self.assertEqual(arr.get(0), "O-001")

        # Delete tengah
        val_prio = arr.delete(2) 
        self.assertEqual(val_prio, "PRIO-001")

        # Bounds check
        with self.assertRaises(IndexError):
            arr.get(999)
        with self.assertRaises(IndexError):
            arr.delete(999)

    def test_linklist_dasar(self):
        ll = LinkList()
        self.assertEqual(len(ll), 0)
        self.assertIsNone(ll.head)
        self.assertIsNone(ll.tail)

        # Append
        for i in range(1, 6):
            ll.append(f"O-{i:03d}")
        self.assertEqual(len(ll), 5)
        self.assertEqual(ll.head.data, "O-001")
        self.assertEqual(ll.tail.data, "O-005")
        self.assertEqual(ll.get(0), "O-001")
        self.assertEqual(ll.get(4), "O-005")

        # Prepend / VIP
        ll.insert_vip("VIP-001")
        self.assertEqual(len(ll), 6)
        self.assertEqual(ll.head.data, "VIP-001")
        self.assertEqual(ll.get(0), "VIP-001")

        # Insert Prioritas 
        ll.insert_prioritas("PRIO-001")
        self.assertEqual(len(ll), 7)
        self.assertEqual(ll.get(3), "PRIO-001")

        # Delete head
        val_vip = ll.delete(0)
        self.assertEqual(val_vip, "VIP-001")
        self.assertEqual(ll.head.data, "O-001")

        # Delete tengah
        val_prio = ll.delete(2)
        self.assertEqual(val_prio, "PRIO-001")

        # Delete tail
        last_idx = len(ll) - 1
        tail_val = ll.get(last_idx)
        val_tail = ll.delete(last_idx)
        self.assertEqual(val_tail, tail_val)
        self.assertEqual(ll.tail.data, ll.get(len(ll) - 1))

        # Bounds check
        with self.assertRaises(IndexError):
            ll.get(999)
        with self.assertRaises(IndexError):
            ll.delete(999)

    def test_kesesuaian_data(self):
        arr = Array(4)
        ll = LinkList()

        pesanan1 = Pesanan("O-101", "Budi", "resto-a", "burger", 20000, 3, 100, None, "ANTRE")
        pesanan2 = Pesanan("O-102", "Siti", "resto-b", "pizza", 45000, 1, 105, None, "ANTRE")

        arr.append(pesanan1)
        ll.append(pesanan1)

        arr.insert_vip(pesanan2)
        ll.insert_vip(pesanan2)

        self.assertEqual(len(arr), len(ll))
        self.assertEqual(arr.get(0).oid, ll.get(0).oid)
        self.assertEqual(arr.get(1).oid, ll.get(1).oid)


if __name__ == "__main__":
    unittest.main()