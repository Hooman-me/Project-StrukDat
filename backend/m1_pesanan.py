# backend/tes.py

import csv
import sys
import os

# Tambahkan path root agar modul dapat diimpor baik secara modular maupun langsung
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from backend.models import Pesanan


class Array:

    def __init__(self, initial_capacity=4):
        self.cap = initial_capacity if initial_capacity > 0 else 4
        self.size = 0
        self.data = [None] * self.cap

    def _resize(self, new_capacity):

        new_data = [None] * new_capacity
        for k in range(self.size):
            new_data[k] = self.data[k]
        self.data = new_data
        self.cap = new_capacity

    def append(self, v):

        if self.size == self.cap:
            self._resize(self.cap * 2)
        self.data[self.size] = v
        self.size += 1

    def insert(self, i, v):

        if i < 0 or i > self.size:
            raise IndexError(f"Indeks di luar batas: {i}, ukuran saat ini: {self.size}")
        if self.size == self.cap:
            self._resize(self.cap * 2)
        
        # Geser seluruh elemen ke kanan dari indeks paling akhir ke i
        for k in range(self.size, i, -1):
            self.data[k] = self.data[k - 1]
        
        self.data[i] = v
        self.size += 1

    def insert_prioritas(self, v):

        self.insert(self.size // 2, v)

    def insert_vip(self, v):

        self.insert(0, v)

    def get(self, i):

        if i < 0 or i >= self.size:
            raise IndexError(f"Indeks di luar batas: {i}, ukuran saat ini: {self.size}")
        return self.data[i]

    def delete(self, i):

        if i < 0 or i >= self.size:
            raise IndexError(f"Indeks di luar batas: {i}, ukuran saat ini: {self.size}")
        removed = self.data[i]
        
        # Geser seluruh elemen ke kiri dari i + 1 hingga akhir
        for k in range(i, self.size - 1):
            self.data[k] = self.data[k + 1]
        
        self.data[self.size - 1] = None
        self.size -= 1
        return removed

    def __len__(self):
        return self.size

    def __getitem__(self, i):
        return self.get(i)

    def __iter__(self):
        for k in range(self.size):
            yield self.data[k]


class Node:

    def __init__(self, data, next_node=None):
        self.data = data
        self.next = next_node


class LinkList:

    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def append(self, v):

        new_node = Node(v)
        if self.head is None:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node
        self.size += 1

    def prepend(self, v):

        new_node = Node(v, self.head)
        self.head = new_node
        if self.tail is None:
            self.tail = new_node
        self.size += 1

    def insert(self, i, v):

        if i < 0 or i > self.size:
            raise IndexError(f"Indeks di luar batas: {i}, ukuran saat ini: {self.size}")
        
        if i == 0:
            self.prepend(v)
            return
        
        if i == self.size:
            self.append(v)
            return

        curr = self.head
        for _ in range(i - 1):
            curr = curr.next

        new_node = Node(v, curr.next)
        curr.next = new_node
        self.size += 1

    def insert_prioritas(self, v):

        self.insert(self.size // 2, v)

    def insert_vip(self, v):

        self.prepend(v)

    def get(self, i):

        if i < 0 or i >= self.size:
            raise IndexError(f"Indeks di luar batas: {i}, ukuran saat ini: {self.size}")
        
        curr = self.head
        for _ in range(i):
            curr = curr.next
        return curr.data

    def delete(self, i):

        if i < 0 or i >= self.size:
            raise IndexError(f"Indeks di luar batas: {i}, ukuran saat ini: {self.size}")
        
        if i == 0:
            removed = self.head.data
            self.head = self.head.next
            if self.head is None:
                self.tail = None
            self.size -= 1
            return removed

        curr = self.head
        for _ in range(i - 1):
            curr = curr.next

        target = curr.next
        removed = target.data
        curr.next = target.next

        if target == self.tail:
            self.tail = curr

        self.size -= 1
        return removed

    def __len__(self):
        return self.size

    def __getitem__(self, i):
        return self.get(i)

    def __iter__(self):
        curr = self.head
        while curr is not None:
            yield curr.data
            curr = curr.next


def muat_pesanan_csv(filepath, limit=None):

    arr = Array(initial_capacity=8)
    ll = LinkList()

    with open(filepath, mode="r", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader, None)  # lewati baris header
        
        count = 0
        for row in reader:
            if not row or len(row) < 9:
                continue
            
            p = Pesanan(
                oid=row[0],
                pelanggan=row[1],
                resto=row[2],
                menu=row[3],
                harga=row[4],
                prioritas=row[5],
                t_masuk_detik=row[6],
                t_selesai_detik=row[7],
                status=row[8]
            )
            arr.append(p)
            ll.append(p)
            
            count += 1
            if limit is not None and count >= limit:
                break

    return (arr, ll)
