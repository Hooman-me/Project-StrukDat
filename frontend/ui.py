import os
import tkinter as tk
from backend.m1_pesanan import (Array, LinkList, Pesanan, baca_csv,
                                tambah_pesanan, ukur)

CSV = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "data", "pesanan.csv")

# (teks menu, struktur, aksi)
MENU = [
    ("DATA - Load CSV", None, "load"),
    ("ARRAY - LIHAT PESANAN", "array", "lihat"),
    ("ARRAY - TAMBAH PESANAN REGULER", "array", "reguler"),
    ("ARRAY - TAMBAH PESANAN PRIORITAS", "array", "prioritas"),
    ("ARRAY - TAMBAH PESANAN VIP", "array", "vip"),
    ("ARRAY - HAPUS PESANAN", "array", "hapus"),
    ("LINKEDLIST - LIHAT PESANAN", "linked", "lihat"),
    ("LINKEDLIST - TAMBAH PESANAN REGULER", "linked", "reguler"),
    ("LINKEDLIST - TAMBAH PESANAN PRIORITAS", "linked", "prioritas"),
    ("LINKEDLIST - TAMBAH PESANAN VIP", "linked", "vip"),
    ("LINKEDLIST - HAPUS PESANAN", "linked", "hapus"),
]
PRIO = {"reguler": 3, "prioritas": 2, "vip": 1}


class Aplikasi:
    def __init__(self, root):
        root.title("2EZ4U Food Delivery")
        root.geometry("950x620")
        self.array = Array()
        self.linked = LinkList()
        self.no_baru = 200001
        self.pilihan = None

        kiri = tk.Frame(root)
        kiri.pack(side="left", fill="y", padx=6, pady=6)
        self.lb = tk.Listbox(kiri, width=42, height=20, exportselection=False)
        for teks, _, _ in MENU:
            self.lb.insert("end", teks)
        self.lb.pack(fill="y", expand=True)
        self.lb.bind("<<ListboxSelect>>", self.pilih_menu)

        kanan = tk.Frame(root)
        kanan.pack(side="right", fill="both", expand=True, padx=6, pady=6)
        self.judul = tk.Label(kanan, text="Pilih menu di kiri", font=("Arial", 13, "bold"))
        self.judul.pack(anchor="w")
        self.form = tk.Frame(kanan)
        self.form.pack(anchor="w", pady=6)
        self.lbl_input = tk.Label(self.form, text="")
        self.entry = tk.Entry(self.form, width=30)
        self.tombol = tk.Button(self.form, text="JALANKAN", command=self.jalankan)
        self.hasil = tk.Text(kanan, height=16)
        self.hasil.pack(fill="both", expand=True)
        tk.Label(kanan, text="COMMAND").pack(anchor="w")
        self.log = tk.Text(kanan, height=8)
        self.log.pack(fill="x")

    def pilih_menu(self, _event):
        idx = self.lb.curselection()
        if not idx:
            return
        teks, struktur, aksi = MENU[idx[0]]
        self.pilihan = (teks, struktur, aksi)
        self.judul.config(text=teks)
        self.lbl_input.pack_forget(); self.entry.pack_forget(); self.tombol.pack_forget()
        self.entry.delete(0, "end")
        if aksi in PRIO:
            self.lbl_input.config(text="Nama pelanggan:")
        elif aksi in ("lihat", "hapus"):
            self.lbl_input.config(text="Nomor urut pesanan (mulai dari 0):")
        if aksi != "load":
            self.lbl_input.pack(side="left"); self.entry.pack(side="left", padx=6)
        self.tombol.pack(side="left")

    def tulis(self, teks):
        self.hasil.delete("1.0", "end")
        self.hasil.insert("end", teks)

    def catat(self, perintah, modul, ms):
        self.log.insert("end", f"{perintah:12s} -> {modul:10s} {ms:10.3f} ms\n")
        self.log.see("end")

    def jalankan(self):
        if self.pilihan is None:
            return
        teks, nama_struktur, aksi = self.pilihan
        s = self.array if nama_struktur == "array" else self.linked
        try:
            if aksi == "load":
                self.muat()
            elif aksi in PRIO:
                nama = self.entry.get().strip() or "Pelanggan Baru"
                oid = "O-%06d" % self.no_baru
                self.no_baru += 1
                p = Pesanan(oid, nama, "-", "-", 0, PRIO[aksi], 0, "", "ANTRE")
                posisi, ms = ukur(tambah_pesanan, s, p)
                self.tulis(f"Ditambahkan di posisi ke-{posisi}\n{p}\nTotal pesanan: {len(s)}")
                self.catat(aksi, nama_struktur, ms)
            elif aksi == "lihat":
                i = int(self.entry.get())
                p, ms = ukur(s.get, i)
                self.tulis(f"Pesanan ke-{i}:\n{p}")
                self.catat("lihat", nama_struktur, ms)
            elif aksi == "hapus":
                i = int(self.entry.get())
                p, ms = ukur(s.hapus, i)
                self.tulis(f"Dihapus:\n{p}\nSisa pesanan: {len(s)}")
                self.catat("hapus", nama_struktur, ms)
        except ValueError:
            self.tulis("Masukkan angka yang valid.")
        except IndexError:
            self.tulis(f"Nomor di luar jangkauan (jumlah pesanan: {len(s)}).")
        except FileNotFoundError:
            self.tulis(f"File tidak ditemukan:\n{CSV}")

    def muat(self):
        data = baca_csv(CSV)
        self.array, self.linked = Array(), LinkList()
        _, ms_a = ukur(lambda: [self.array.append(p) for p in data])
        _, ms_l = ukur(lambda: [self.linked.append(p) for p in data])
        self.tulis(f"Berhasil memuat {len(data)} pesanan ke Array dan LinkedList.")
        self.catat("load", "array", ms_a)
        self.catat("load", "linked", ms_l)