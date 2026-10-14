# backend/m2_antrean.py

import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)


class Stack:
    """Implementasi struktur data Tumpukan (LIFO) berbasis larik dinamis."""

    def __init__(self, cap=8):
        self.cap = cap if cap > 0 else 8
        self.size = 0
        self.data = [None] * self.cap

    def _grow(self):
        new_cap = self.cap * 2
        baru = [None] * new_cap
        for i in range(self.size):
            baru[i] = self.data[i]
        self.data = baru
        self.cap = new_cap

    def push(self, x):
        if self.size == self.cap:
            self._grow()
        self.data[self.size] = x
        self.size += 1

    def pop(self):
        if self.size == 0:
            return None
        self.size -= 1
        x = self.data[self.size]
        self.data[self.size] = None
        return x

    def peek(self):
        if self.size == 0:
            return None
        return self.data[self.size - 1]

    def is_empty(self):
        return self.size == 0

    def kosong(self):
        return self.size == 0

    def to_list(self):
        hasil = []
        for i in range(self.size):
            hasil.append(self.data[i])
        return hasil

    def __len__(self):
        return self.size


class AntreanNaif:
    """Antrean versi naif di atas larik biasa.
    
    Operasi dequeue mengambil elemen depan (indeks 0) dan menggeser seluruh
    elemen yang tersisa satu langkah ke kiri (kompleksitas O(n)).
    """

    def __init__(self, cap=8):
        self.cap = cap if cap > 0 else 8
        self.size = 0
        self.data = [None] * self.cap
        self.total_geseran = 0
        self.geseran_terakhir = 0

    def _grow(self):
        new_cap = self.cap * 2
        baru = [None] * new_cap
        for i in range(self.size):
            baru[i] = self.data[i]
        self.data = baru
        self.cap = new_cap

    def enqueue(self, x):
        """Menambahkan elemen di belakang antrean. Kompleksitas O(1)."""
        if self.size == self.cap:
            self._grow()
        self.data[self.size] = x
        self.size += 1

    def dequeue(self):
        """Mengambil elemen depan dengan menggeser seluruh sisa elemen ke kiri. Kompleksitas O(n)."""
        if self.size == 0:
            self.geseran_terakhir = 0
            return None
        
        elemen = self.data[0]
        # Geser seluruh sisa elemen ke kiri
        geseran = 0
        for i in range(1, self.size):
            self.data[i - 1] = self.data[i]
            geseran += 1
        
        self.size -= 1
        self.data[self.size] = None
        self.geseran_terakhir = geseran
        self.total_geseran += geseran
        return elemen

    def enqueue_depan(self, x):
        """Menyisipkan kembali di depan (digunakan untuk operasi pembatalan / undo)."""
        if self.size == self.cap:
            self._grow()
        for i in range(self.size, 0, -1):
            self.data[i] = self.data[i - 1]
        self.data[0] = x
        self.size += 1

    def dequeue_belakang(self):
        """Mengeluarkan dari belakang (digunakan untuk pembatalan enqueue)."""
        if self.size == 0:
            return None
        self.size -= 1
        x = self.data[self.size]
        self.data[self.size] = None
        return x

    def peek(self):
        if self.size == 0:
            return None
        return self.data[0]

    def is_empty(self):
        return self.size == 0

    def __len__(self):
        return self.size


class AntreanMelingkar:
    """Antrean versi melingkar (Circular Queue) berbasis larik berputar.
    
    Menggunakan penunjuk front dan rear dengan operasi modulo.
    Operasi dequeue hanya memajukan front tanpa menggeser elemen apa pun (O(1)).
    """

    def __init__(self, cap=8):
        self.cap = cap if cap > 0 else 8
        self.count = 0
        self.front = 0
        self.rear = 0
        self.data = [None] * self.cap
        self.total_geseran = 0
        self.geseran_terakhir = 0

    def _grow(self):
        new_cap = self.cap * 2
        baru = [None] * new_cap
        for i in range(self.count):
            baru[i] = self.data[(self.front + i) % self.cap]
        self.data = baru
        self.cap = new_cap
        self.front = 0
        self.rear = self.count

    def enqueue(self, x):
        """Menambahkan elemen di belakang antrean (rear). Kompleksitas O(1)."""
        if self.count == self.cap:
            self._grow()
        self.data[self.rear] = x
        self.rear = (self.rear + 1) % self.cap
        self.count += 1

    def dequeue(self):
        """Mengambil elemen depan (front) tanpa menggeser elemen. Kompleksitas O(1)."""
        if self.count == 0:
            self.geseran_terakhir = 0
            return None
        
        elemen = self.data[self.front]
        self.data[self.front] = None
        self.front = (self.front + 1) % self.cap
        self.count -= 1
        self.geseran_terakhir = 0
        return elemen

    def enqueue_depan(self, x):
        """Menyisipkan kembali di depan (digunakan untuk operasi undo dequeue)."""
        if self.count == self.cap:
            self._grow()
        self.front = (self.front - 1 + self.cap) % self.cap
        self.data[self.front] = x
        self.count += 1

    def dequeue_belakang(self):
        """Mengeluarkan dari belakang (digunakan untuk pembatalan enqueue)."""
        if self.count == 0:
            return None
        self.rear = (self.rear - 1 + self.cap) % self.cap
        x = self.data[self.rear]
        self.data[self.rear] = None
        self.count -= 1
        return x

    def peek(self):
        if self.count == 0:
            return None
        return self.data[self.front]

    def is_empty(self):
        return self.count == 0

    @property
    def size(self):
        return self.count

    def __len__(self):
        return self.count


# Alias kompatibilitas
Queue = AntreanMelingkar


# ---------------------------------------------------------------------------
# Mesin Kasir: Tokenisasi, Konversi Infix ke Postfix, dan Evaluasi Postfix
# ---------------------------------------------------------------------------

def _presedensi(op):
    if op == "*" or op == "/":
        return 2
    elif op == "+" or op == "-":
        return 1
    return 0


def pisah_token(ekspresi):
    """Memecah string ekspresi menjadi daftar token angka, operator, dan tanda kurung."""
    tokens = []
    i = 0
    n = len(ekspresi)
    while i < n:
        c = ekspresi[i]
        if c == " " or c == "\t" or c == "\r" or c == "\n":
            i += 1
            continue
        if c.isdigit():
            j = i
            while j < n and ekspresi[j].isdigit():
                j += 1
            tokens.append(ekspresi[i:j])
            i = j
        elif c in ("+", "-", "*", "/", "(", ")"):
            tokens.append(c)
            i += 1
        else:
            i += 1
    return tokens


def ke_postfix(ekspresi):
    """Mengubah ekspresi infix menjadi postfix menggunakan tumpukan operator.
    
    Mengembalikan tuple: (list_token_postfix, string_postfix, tabel_langkah)
    """
    tokens = pisah_token(ekspresi)
    stack = Stack()
    keluaran = []
    langkah = []

    no = 1
    for t in tokens:
        if t.isdigit():
            keluaran.append(t)
            tindakan = "angka, langsung keluar"
        elif t == "(":
            stack.push(t)
            tindakan = "push ("
        elif t == ")":
            while not stack.is_empty() and stack.peek() != "(":
                keluaran.append(stack.pop())
            if not stack.is_empty() and stack.peek() == "(":
                stack.pop() # buang tanda '('
            tindakan = "pop sampai ( , buang ("
        elif t in ("+", "-", "*", "/", "%"):
            p_curr = _presedensi(t)
            while not stack.is_empty() and stack.peek() != "(" and _presedensi(stack.peek()) >= p_curr:
                keluaran.append(stack.pop())
            stack.push(t)
            tindakan = f"push {t}"
        else:
            tindakan = f"abaikan {t}"

        # Catat status stack saat ini
        stack_str = " ".join(stack.to_list()) if len(stack) > 0 else "kosong"
        out_str = " ".join(keluaran)
        langkah.append((f"1.{no}", t, tindakan, stack_str, out_str))
        no += 1

    # Pop sisa operator di stack
    while not stack.is_empty():
        top = stack.pop()
        if top != "(":
            keluaran.append(top)
    
    langkah.append(("1.akhir", "-", "pop sisa stack", "kosong", " ".join(keluaran)))
    str_postfix = " ".join(keluaran)
    return (keluaran, str_postfix, langkah)


def hitung(postfix):
    """Mengevaluasi ekspresi postfix menggunakan tumpukan angka.
    
    Mengembalikan tuple: (total_nilai, tabel_langkah)
    """
    if isinstance(postfix, str):
        tokens = pisah_token(postfix)
    else:
        tokens = postfix

    stack = Stack()
    langkah = []
    no = 1

    for t in tokens:
        if t.isdigit():
            nilai = int(t)
            stack.push(nilai)
            stack_str = " ".join([str(x) for x in stack.to_list()])
            langkah.append((f"2.{no}", t, f"push {nilai}", stack_str, "-"))
        elif t in ("+", "-", "*", "/"):
            # Perhatikan urutan pop: b (kanan) keluar duluan, lalu a (kiri)
            b = stack.pop()
            a = stack.pop()
            if a is None or b is None:
                continue
            
            if t == "+":
                res = a + b
            elif t == "-":
                res = a - b
            elif t == "*":
                res = a * b
            elif t == "/":
                res = a // b if b != 0 else 0
            
            stack.push(res)
            stack_str = " ".join([str(x) for x in stack.to_list()])
            tindakan = f"pop {b} dan {a} -> {a}{t}{b} = {res}"
            langkah.append((f"2.{no}", t, tindakan, stack_str, str(res)))
        no += 1

    total = stack.pop() if not stack.is_empty() else 0
    return (total, langkah)


# ---------------------------------------------------------------------------
# Pengelola Antrean & Riwayat Undo/Redo untuk Antarmuka
# ---------------------------------------------------------------------------

class PengelolaAntrean:
    """Mengelola pasangan Antrean Naif & Melingkar serta tumpukan Undo & Redo."""

    def __init__(self):
        self.naif = AntreanNaif()
        self.circular = AntreanMelingkar()
        self.stack_undo = Stack()
        self.stack_redo = Stack()

    def muat_dari_list(self, daftar_pesanan):
        """Memasukkan pesanan berstatus ANTRE ke kedua antrean."""
        self.naif = AntreanNaif(cap=len(daftar_pesanan) + 8)
        self.circular = AntreanMelingkar(cap=len(daftar_pesanan) + 8)
        self.stack_undo = Stack()
        self.stack_redo = Stack()
        
        for p in daftar_pesanan:
            if p.status == "ANTRE":
                self.naif.enqueue(p)
                self.circular.enqueue(p)

    def enqueue(self, pesanan):
        """Menambahkan satu pesanan ke kedua antrean."""
        self.naif.enqueue(pesanan)
        self.circular.enqueue(pesanan)
        # Catat aksi ke undo, kosongkan redo
        self.stack_undo.push(("ENQUEUE", pesanan))
        self.stack_redo = Stack()

    def dequeue_naif(self, jumlah=1):
        """Melayani n pesanan dari antrean naif."""
        hasil = []
        for _ in range(jumlah):
            if self.naif.is_empty():
                break
            p = self.naif.dequeue()
            if p is not None:
                hasil.append(p)
        return hasil

    def dequeue_circular(self, jumlah=1):
        """Melayani n pesanan dari antrean circular."""
        hasil = []
        for _ in range(jumlah):
            if self.circular.is_empty():
                break
            p = self.circular.dequeue()
            if p is not None:
                hasil.append(p)
        
        if len(hasil) > 0:
            self.stack_undo.push(("DEQUEUE", hasil))
            self.stack_redo = Stack()
            
        return hasil

    def undo_last(self):
        """Membatalkan aksi terakhir."""
        if self.stack_undo.is_empty():
            return None
        
        aksi, data = self.stack_undo.pop()
        
        if aksi == "ENQUEUE":
            # Keluarkan kembali pesanan dari belakang antrean circular & naif
            p_circ = self.circular.dequeue_belakang()
            p_naif = self.naif.dequeue_belakang()
            self.stack_redo.push(("ENQUEUE", data))
            return ("ENQUEUE", data)
            
        elif aksi == "DEQUEUE":
            # Kembalikan daftar pesanan yang baru keluar ke depan antrean circular & naif
            # Urutan pengembalian dibalik agar urutan semula tetap terjaga
            daftar = data
            for i in range(len(daftar) - 1, -1, -1):
                p = daftar[i]
                self.circular.enqueue_depan(p)
                self.naif.enqueue_depan(p)
            self.stack_redo.push(("DEQUEUE", data))
            return ("DEQUEUE", data)

        return None

    def redo_last(self):
        """Mengerjakan ulang aksi yang baru saja dibatalkan."""
        if self.stack_redo.is_empty():
            return None
        
        aksi, data = self.stack_redo.pop()
        
        if aksi == "ENQUEUE":
            self.circular.enqueue(data)
            self.naif.enqueue(data)
            self.stack_undo.push(("ENQUEUE", data))
            return ("ENQUEUE", data)
            
        elif aksi == "DEQUEUE":
            daftar = data
            for _ in range(len(daftar)):
                self.circular.dequeue()
                self.naif.dequeue()
            self.stack_undo.push(("DEQUEUE", data))
            return ("DEQUEUE", data)

        return None
