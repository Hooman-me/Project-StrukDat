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

    def kembalikan_ke_depan(self, daftar):
        """Mengembalikan daftar elemen ke depan antrean dengan menggeser elemen sekali jalan.
        
        Seluruh elemen yang ada digeser sekaligus sejauh len(daftar) posisi ke kanan,
        bukan sekali per elemen.
        """
        k = len(daftar)
        if k == 0:
            return
        while self.size + k > self.cap:
            self._grow()
        # Geser seluruh elemen ke kanan sejauh k posisi sekaligus
        geseran = self.size
        for i in range(self.size - 1, -1, -1):
            self.data[i + k] = self.data[i]
        for j in range(k):
            self.data[j] = daftar[j]
        self.size += k
        self.geseran_terakhir = geseran
        self.total_geseran += geseran

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
    
    Keputusan Desain:
    1. Memakai atribut count: Membedakan kondisi antrean penuh (count == cap) dan
       kosong (count == 0) secara tegas tanpa perlu mengorbankan 1 slot kosong larik.
    2. Antrean tumbuh saat penuh: Saat count == cap, antrean melakukan penggandaan
       kapasitas (_grow) sebesar 2x lipat dan menata ulang posisi elemen dari indeks 0,
       sehingga antrean bersifat dinamis dan tidak terjadi overflow.
    
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

    def kembalikan_ke_depan(self, daftar):
        """Mengembalikan daftar elemen ke depan antrean circular (hanya memundurkan front)."""
        k = len(daftar)
        if k == 0:
            return
        while self.count + k > self.cap:
            self._grow()
        self.front = (self.front - k + self.cap) % self.cap
        for i in range(k):
            self.data[(self.front + i) % self.cap] = daftar[i]
        self.count += k
        self.geseran_terakhir = 0

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
            raise ValueError(f"Karakter asing atau tidak valid ditemukan: '{c}'")
    return tokens


def ke_postfix(ekspresi):
    """Mengubah ekspresi infix menjadi postfix menggunakan tumpukan operator.
    
    Mengembalikan tuple: (list_token_postfix, string_postfix, tabel_langkah)
    """
    if isinstance(ekspresi, str):
        tokens = pisah_token(ekspresi)
    else:
        tokens = ekspresi

    if not tokens:
        raise ValueError("Ekspresi aritmatika kosong.")

    # Validasi operator di ujung (awal atau akhir ekspresi)
    op_biner = ("+", "-", "*", "/")
    if tokens[0] in op_biner:
        raise ValueError(f"Operator tidak boleh berada di ujung awal ekspresi: '{tokens[0]}'")
    if tokens[-1] in op_biner:
        raise ValueError(f"Operator tidak boleh berada di ujung akhir ekspresi: '{tokens[-1]}'")

    # Validasi sintaksis: dua angka berurutan, operator berurutan, posisi kurung
    for idx in range(len(tokens) - 1):
        curr_t = tokens[idx]
        next_t = tokens[idx + 1]
        if curr_t.isdigit() and next_t.isdigit():
            raise ValueError(f"Dua angka berurutan tanpa operator: '{curr_t}' dan '{next_t}'")
        if curr_t in op_biner and next_t in op_biner:
            raise ValueError(f"Dua operator berurutan: '{curr_t}' dan '{next_t}'")
        if curr_t == "(" and next_t in op_biner:
            raise ValueError(f"Operator langsung setelah kurung buka: '({next_t}'")
        if curr_t in op_biner and next_t == ")":
            raise ValueError(f"Operator langsung sebelum kurung tutup: '{curr_t})'")
        if curr_t == "(" and next_t == ")":
            raise ValueError("Tanda kurung kosong '()'")

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
            found_open = False
            while not stack.is_empty():
                top = stack.pop()
                if top == "(":
                    found_open = True
                    break
                keluaran.append(top)
            if not found_open:
                raise ValueError("Kurung tak berpasangan: tanda kurung tutup ')' berlebih.")
            tindakan = "pop sampai ( , buang ("
        elif t in ("+", "-", "*", "/", "%"):
            p_curr = _presedensi(t)
            popped_ops = []
            while not stack.is_empty() and stack.peek() != "(" and _presedensi(stack.peek()) >= p_curr:
                op = stack.pop()
                keluaran.append(op)
                popped_ops.append(op)
            stack.push(t)
            if popped_ops:
                pop_parts = [f"pop {op} (lebih kuat/sama kuat)" for op in popped_ops]
                tindakan = f"{', '.join(pop_parts)}, push {t}"
            else:
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
        if top == "(":
            raise ValueError("Kurung tak berpasangan: tanda kurung buka '(' tidak memiliki pasangan tutup.")
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

    if not tokens:
        raise ValueError("Ekspresi postfix kosong.")

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
            if len(stack) < 2:
                raise ValueError(f"Operand kurang untuk operator '{t}'.")
            b = stack.pop()
            a = stack.pop()
            
            if t == "+":
                res = a + b
            elif t == "-":
                res = a - b
            elif t == "*":
                res = a * b
            elif t == "/":
                if b == 0:
                    raise ValueError("Pembagian dengan nol tidak diperbolehkan.")
                res = a // b
            
            stack.push(res)
            stack_str = " ".join([str(x) for x in stack.to_list()])
            tindakan = f"pop {b} dan {a} -> {a}{t}{b} = {res}"
            langkah.append((f"2.{no}", t, tindakan, stack_str, str(res)))
        else:
            raise ValueError(f"Token postfix tidak dikenali: '{t}'")
        no += 1

    if stack.is_empty():
        raise ValueError("Ekspresi tidak menghasilkan nilai.")

    total = stack.pop()
    if not stack.is_empty():
        raise ValueError("Operand berlebih atau operator kurang dalam ekspresi.")

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
        self.naif = AntreanNaif(cap=8)
        self.circular = AntreanMelingkar(cap=8)
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
        
        if len(hasil) > 0:
            self.stack_undo.push(("DEQUEUE_NAIF", hasil))
            self.stack_redo = Stack()

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
            self.stack_undo.push(("DEQUEUE_CIRCULAR", hasil))
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
            
        elif aksi == "DEQUEUE_NAIF":
            self.naif.kembalikan_ke_depan(data)
            self.stack_redo.push(("DEQUEUE_NAIF", data))
            return ("DEQUEUE_NAIF", data)

        elif aksi == "DEQUEUE_CIRCULAR":
            self.circular.kembalikan_ke_depan(data)
            self.stack_redo.push(("DEQUEUE_CIRCULAR", data))
            return ("DEQUEUE_CIRCULAR", data)

        elif aksi == "DEQUEUE":
            # Kompatibilitas jika ada aksi bertipe DEQUEUE umum
            self.circular.kembalikan_ke_depan(data)
            self.naif.kembalikan_ke_depan(data)
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
            
        elif aksi == "DEQUEUE_NAIF":
            daftar = data
            for _ in range(len(daftar)):
                self.naif.dequeue()
            self.stack_undo.push(("DEQUEUE_NAIF", data))
            return ("DEQUEUE_NAIF", data)

        elif aksi == "DEQUEUE_CIRCULAR":
            daftar = data
            for _ in range(len(daftar)):
                self.circular.dequeue()
            self.stack_undo.push(("DEQUEUE_CIRCULAR", data))
            return ("DEQUEUE_CIRCULAR", data)

        elif aksi == "DEQUEUE":
            daftar = data
            for _ in range(len(daftar)):
                self.circular.dequeue()
                self.naif.dequeue()
            self.stack_undo.push(("DEQUEUE", data))
            return ("DEQUEUE", data)

        return None

    def history(self):
        """Mengembalikan daftar riwayat aksi yang tersimpan pada tumpukan undo."""
        return self.stack_undo.to_list()

    def stats(self):
        """Mengembalikan statistik antrean sebagai list of tuple (label, nilai).
        
        Catatan: Menggunakan list tuple karena struktur dict dilarang sesuai spesifikasi.
        """
        return [
            ("panjang_naif", len(self.naif)),
            ("panjang_circular", len(self.circular)),
            ("kapasitas_naif", self.naif.cap),
            ("kapasitas_circular", self.circular.cap),
            ("total_geseran_naif", self.naif.total_geseran),
            ("total_geseran_circular", self.circular.total_geseran),
            ("undo_depth", len(self.stack_undo)),
            ("redo_depth", len(self.stack_redo)),
        ]
