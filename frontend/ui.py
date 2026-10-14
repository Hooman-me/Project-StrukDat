# frontend/ui.py

import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from backend.models import Pesanan
from backend.m1_pesanan import (
    Array, LinkList, muat_pesanan_csv, tambah_pesanan, ukur
)
from backend.m2_antrean import (
    PengelolaAntrean, ke_postfix, hitung
)
from backend.m3_laporan import (
    insertion_sort, merge_sort, linear_search, binary_search
)

CSV_PATH = os.path.join(parent_dir, "data", "pesanan.csv")

# Daftar Menu: (label_tampilan, kategori, id_aksi)
MENU_ITEMS = [
    # DATA
    ("DATA - Load CSV", "data", "load"),
    # M1 - DATA PESANAN
    ("ARRAY - LIHAT PESANAN", "m1_array", "lihat"),
    ("ARRAY - TAMBAH PESANAN REGULER", "m1_array", "tambah_reguler"),
    ("ARRAY - TAMBAH PESANAN PRIORITAS", "m1_array", "tambah_prioritas"),
    ("ARRAY - TAMBAH PESANAN VIP", "m1_array", "tambah_vip"),
    ("ARRAY - HAPUS PESANAN", "m1_array", "hapus"),
    ("LINKEDLIST - LIHAT PESANAN", "m1_linked", "lihat"),
    ("LINKEDLIST - TAMBAH PESANAN REGULER", "m1_linked", "tambah_reguler"),
    ("LINKEDLIST - TAMBAH PESANAN PRIORITAS", "m1_linked", "tambah_prioritas"),
    ("LINKEDLIST - TAMBAH PESANAN VIP", "m1_linked", "tambah_vip"),
    ("LINKEDLIST - HAPUS PESANAN", "m1_linked", "hapus"),
    # M2 - STACK DAN QUEUE
    ("STACK - POSTFIX (MESIN KASIR)", "m2_stack", "postfix"),
    ("STACK - UNDO", "m2_stack", "undo"),
    ("STACK - REDO", "m2_stack", "redo"),
    ("QUEUE - ENQUEUE", "m2_queue", "enqueue"),
    ("QUEUE - DEQUEUE NAIF", "m2_queue", "dequeue_naif"),
    ("QUEUE - DEQUEUE CIRCULAR", "m2_queue", "dequeue_circular"),
    # M3 - SORT DAN SEARCH
    ("SORT - INSERTION SORT", "m3_sort", "insertion_sort"),
    ("SORT - MERGE SORT", "m3_sort", "merge_sort"),
    ("SEARCH - LINEAR SEARCH", "m3_search", "linear_search"),
    ("SEARCH - BINARY SEARCH", "m3_search", "binary_search"),
]


class AppUI:
    """Antarmuka pengguna Tkinter untuk sistem 2EZ4U Food Delivery."""

    def __init__(self, root):
        self.root = root
        self.root.title("2EZ4U Food Delivery")
        self.root.geometry("1020x680")
        self.root.minsize(920, 600)

        # State data
        self.array_pesanan = Array(initial_capacity=8)
        self.linklist_pesanan = LinkList()
        self.raw_data = []           # Python list murni untuk pemuatan
        self.antrean_manager = PengelolaAntrean()
        self.daftar_terurut_oid = None # Cache untuk binary search
        self.no_baru = 200001
        self.menu_terpilih = None

        self._buat_layout()
        self._pilih_menu_awal()

    def _buat_layout(self):
        # Header banner
        header = tk.Frame(self.root, bg="#1e293b", height=42)
        header.pack(side="top", fill="x")
        lbl_brand = tk.Label(
            header, text="2EZ4U Food Delivery", font=("Arial", 13, "bold"),
            fg="#f8fafc", bg="#1e293b", padx=12, pady=8
        )
        lbl_brand.pack(side="left")

        # Container Utama (Kiri: Navigasi, Kanan: Konten Kerja)
        kontainer = tk.Frame(self.root)
        kontainer.pack(side="top", fill="both", expand=True, padx=8, pady=8)

        # Panel Kiri (Daftar Menu)
        panel_kiri = tk.Frame(kontainer, width=280)
        panel_kiri.pack(side="left", fill="y", padx=(0, 8))

        lbl_menu = tk.Label(panel_kiri, text="DAFTAR PERINTAH", font=("Arial", 9, "bold"), fg="#475569")
        lbl_menu.pack(anchor="w", pady=(0, 4))

        frame_lb = tk.Frame(panel_kiri)
        frame_lb.pack(fill="both", expand=True)

        scroll_lb = tk.Scrollbar(frame_lb, orient="vertical")
        self.lb_menu = tk.Listbox(
            frame_lb, width=36, font=("Consolas", 9), selectmode="single",
            exportselection=False, yscrollcommand=scroll_lb.set
        )
        scroll_lb.config(command=self.lb_menu.yview)
        scroll_lb.pack(side="right", fill="y")
        self.lb_menu.pack(side="left", fill="both", expand=True)

        for teks, _, _ in MENU_ITEMS:
            self.lb_menu.insert("end", teks)
        self.lb_menu.bind("<<ListboxSelect>>", self._on_menu_dipilih)

        # Panel Kanan (Form, Hasil, dan Log Command)
        panel_kanan = tk.Frame(kontainer)
        panel_kanan.pack(side="right", fill="both", expand=True)

        # Bagian Judul dan Deskripsi
        self.lbl_judul = tk.Label(panel_kanan, text="Silakan pilih menu di kiri", font=("Arial", 12, "bold"))
        self.lbl_judul.pack(anchor="w")

        self.lbl_deskripsi = tk.Label(panel_kanan, text="", font=("Arial", 9), fg="#64748b", wraplength=650, justify="left")
        self.lbl_deskripsi.pack(anchor="w", pady=(2, 6))

        # Bagian Form Parameter Dinamis
        self.frame_form = tk.Frame(panel_kanan, relief="groove", bd=1, padx=8, pady=8)
        self.frame_form.pack(fill="x", pady=(0, 6))

        # Komponen form dinamis
        self.lbl_param1 = tk.Label(self.frame_form, text="Parameter:")
        self.entry_param1 = tk.Entry(self.frame_form, width=32)

        self.lbl_param2 = tk.Label(self.frame_form, text="Kunci:")
        self.var_kunci = tk.StringVar(value="harga")
        self.cb_kunci = ttk.Combobox(
            self.frame_form, textvariable=self.var_kunci,
            values=["harga", "oid", "selesai"], width=12, state="readonly"
        )

        self.btn_aksi = tk.Button(
            self.frame_form, text="JALANKAN", font=("Arial", 9, "bold"),
            bg="#2563eb", fg="white", padx=12, pady=4, cursor="hand2",
            command=self.jalankan_perintah
        )

        # Area Hasil / Output Teks
        lbl_res = tk.Label(panel_kanan, text="HASIL EKSEKUSI", font=("Arial", 9, "bold"), fg="#475569")
        lbl_res.pack(anchor="w", pady=(4, 2))

        frame_hasil = tk.Frame(panel_kanan)
        frame_hasil.pack(fill="both", expand=True)

        scroll_hasil_y = tk.Scrollbar(frame_hasil, orient="vertical")
        scroll_hasil_x = tk.Scrollbar(frame_hasil, orient="horizontal")
        self.txt_hasil = tk.Text(
            frame_hasil, font=("Consolas", 9), wrap="none",
            xscrollcommand=scroll_hasil_x.set, yscrollcommand=scroll_hasil_y.set
        )
        scroll_hasil_y.config(command=self.txt_hasil.yview)
        scroll_hasil_x.config(command=self.txt_hasil.xview)
        scroll_hasil_y.pack(side="right", fill="y")
        scroll_hasil_x.pack(side="bottom", fill="x")
        self.txt_hasil.pack(side="left", fill="both", expand=True)

        # Panel COMMAND (Log Riwayat Perintah)
        lbl_cmd = tk.Label(panel_kanan, text="PANEL COMMAND (WAKTU EKSEKUSI)", font=("Arial", 9, "bold"), fg="#475569")
        lbl_cmd.pack(anchor="w", pady=(6, 2))

        frame_log = tk.Frame(panel_kanan)
        frame_log.pack(fill="x")
        scroll_log = tk.Scrollbar(frame_log, orient="vertical")
        self.txt_log = tk.Text(frame_log, height=5, font=("Consolas", 8), bg="#0f172a", fg="#38bdf8", yscrollcommand=scroll_log.set)
        scroll_log.config(command=self.txt_log.yview)
        scroll_log.pack(side="right", fill="y")
        self.txt_log.pack(side="left", fill="both", expand=True)

        # Baris Status di paling bawah
        self.lbl_status = tk.Label(
            self.root, text="Status: Siap. Silakan klik menu DATA - Load CSV terlebih dahulu.",
            font=("Arial", 8), bd=1, relief="sunken", anchor="w", padx=6, pady=3, bg="#f1f5f9"
        )
        self.lbl_status.pack(side="bottom", fill="x")

    def _pilih_menu_awal(self):
        self.lb_menu.selection_set(0)
        self._on_menu_dipilih(None)

    def _on_menu_dipilih(self, _event):
        sel = self.lb_menu.curselection()
        if not sel:
            return
        idx = sel[0]
        teks, kat, aksi = MENU_ITEMS[idx]
        self.menu_terpilih = (teks, kat, aksi)

        self.lbl_judul.config(text=teks)
        self._sembunyikan_semua_form()

        # Konfigurasi form berdasarkan menu aksi
        if aksi == "load":
            self.lbl_deskripsi.config(text="Memuat seluruh data dari pesanan.csv (200.000 baris) ke dalam memori.")
            self.btn_aksi.config(text="MUAT DATA")
            self.btn_aksi.pack(side="left", padx=4)

        elif aksi == "lihat":
            self.lbl_deskripsi.config(text="Membuka detail satu pesanan berdasarkan nomor urut (indeks 0..n-1).")
            self.lbl_param1.config(text="Nomor urut (indeks mulai dari 0):")
            self.entry_param1.delete(0, "end")
            self.entry_param1.insert(0, "0")
            self.lbl_param1.pack(side="left", padx=2)
            self.entry_param1.pack(side="left", padx=6)
            self.btn_aksi.config(text="LIHAT")
            self.btn_aksi.pack(side="left", padx=4)

        elif aksi in ("tambah_reguler", "tambah_prioritas", "tambah_vip"):
            prio_text = "REGULER (paling belakang)" if "reguler" in aksi else ("PRIORITAS (tengah barisan)" if "prioritas" in aksi else "VIP (paling depan)")
            self.lbl_deskripsi.config(text=f"Menambahkan pesanan baru dengan prioritas {prio_text}.")
            self.lbl_param1.config(text="Nama pelanggan:")
            self.entry_param1.delete(0, "end")
            self.entry_param1.insert(0, "Pelanggan Baru")
            self.lbl_param1.pack(side="left", padx=2)
            self.entry_param1.pack(side="left", padx=6)
            self.btn_aksi.config(text="TAMBAH")
            self.btn_aksi.pack(side="left", padx=4)

        elif aksi == "hapus":
            self.lbl_deskripsi.config(text="Menghapus pesanan pada nomor urut tertentu dari barisan.")
            self.lbl_param1.config(text="Nomor urut pesanan yang akan dihapus:")
            self.entry_param1.delete(0, "end")
            self.entry_param1.insert(0, "0")
            self.lbl_param1.pack(side="left", padx=2)
            self.entry_param1.pack(side="left", padx=6)
            self.btn_aksi.config(text="HAPUS")
            self.btn_aksi.pack(side="left", padx=4)

        elif aksi == "postfix":
            self.lbl_deskripsi.config(text="Menghitung struk kasir: konversi infix ke postfix lalu evaluasi menggunakan stack.")
            self.lbl_param1.config(text="Struk belanja (infix):")
            self.entry_param1.delete(0, "end")
            self.entry_param1.insert(0, "( 3 * 12000 ) + ( 2 * 8500 ) - 5000")
            self.lbl_param1.pack(side="left", padx=2)
            self.entry_param1.pack(side="left", padx=6)
            self.btn_aksi.config(text="HITUNG")
            self.btn_aksi.pack(side="left", padx=4)

        elif aksi == "undo":
            self.lbl_deskripsi.config(text="Membatalkan aksi antrean terakhir (pop dari tumpukan undo lalu balikkan aksinya).")
            self.btn_aksi.config(text="UNDO")
            self.btn_aksi.pack(side="left", padx=4)

        elif aksi == "redo":
            self.lbl_deskripsi.config(text="Mengerjakan ulang aksi antrean yang baru saja dibatalkan (pop dari tumpukan redo).")
            self.btn_aksi.config(text="REDO")
            self.btn_aksi.pack(side="left", padx=4)

        elif aksi == "enqueue":
            self.lbl_deskripsi.config(text="Menambahkan satu pesanan berstatus ANTRE ke belakang KEDUA antrean (naif & circular).")
            self.lbl_param1.config(text="Nama pelanggan:")
            self.entry_param1.delete(0, "end")
            self.entry_param1.insert(0, "Pelanggan Baru")
            self.lbl_param1.pack(side="left", padx=2)
            self.entry_param1.pack(side="left", padx=6)
            self.btn_aksi.config(text="ENQUEUE")
            self.btn_aksi.pack(side="left", padx=4)

        elif aksi in ("dequeue_naif", "dequeue_circular"):
            tipe = "naif (geser seluruh elemen, O(n))" if aksi == "dequeue_naif" else "circular (hanya majukan front, O(1))"
            self.lbl_deskripsi.config(text=f"Melayani pesanan terdepan menggunakan antrean {tipe}.")
            self.lbl_param1.config(text="Berapa kali dequeue:")
            self.entry_param1.delete(0, "end")
            self.entry_param1.insert(0, "1")
            self.lbl_param1.pack(side="left", padx=2)
            self.entry_param1.pack(side="left", padx=6)
            self.btn_aksi.config(text="DEQUEUE")
            self.btn_aksi.pack(side="left", padx=4)

        elif aksi in ("insertion_sort", "merge_sort"):
            tipe = "Insertion Sort (O(n^2), batas 20.000 data)" if aksi == "insertion_sort" else "Merge Sort (O(n log n), sanggup 200.000 data)"
            self.lbl_deskripsi.config(text=f"Mengurutkan laporan pesanan menggunakan {tipe}.")
            self.lbl_param1.config(text="Jumlah baris diurutkan:")
            self.entry_param1.delete(0, "end")
            self.entry_param1.insert(0, "2000" if aksi == "insertion_sort" else "4000")
            self.lbl_param1.pack(side="left", padx=2)
            self.entry_param1.pack(side="left", padx=4)
            self.lbl_param2.pack(side="left", padx=(8, 2))
            self.cb_kunci.pack(side="left", padx=4)
            self.btn_aksi.config(text="URUTKAN")
            self.btn_aksi.pack(side="left", padx=6)

        elif aksi in ("linear_search", "binary_search"):
            tipe = "Linear Search (O(n), data tidak perlu terurut)" if aksi == "linear_search" else "Binary Search (O(log n), data harus terurut)"
            self.lbl_deskripsi.config(text=f"Mencari pesanan berdasarkan ID menggunakan {tipe}.")
            self.lbl_param1.config(text="Nomor pesanan (oid):")
            self.entry_param1.delete(0, "end")
            self.entry_param1.insert(0, "O-137442")
            self.lbl_param1.pack(side="left", padx=2)
            self.entry_param1.pack(side="left", padx=6)
            self.btn_aksi.config(text="CARI")
            self.btn_aksi.pack(side="left", padx=4)

    def _sembunyikan_semua_form(self):
        self.lbl_param1.pack_forget()
        self.entry_param1.pack_forget()
        self.lbl_param2.pack_forget()
        self.cb_kunci.pack_forget()
        self.btn_aksi.pack_forget()

    def tulis_hasil(self, teks):
        self.txt_hasil.delete("1.0", "end")
        self.txt_hasil.insert("end", teks)

    def catat_command(self, perintah, modul, ms, detail=""):
        baris = f"{perintah:<24s} -> {modul:<16s} {ms:>8.2f} ms\n"
        self.txt_log.insert("end", baris)
        self.txt_log.see("end")
        status_teks = f"[{modul}] {perintah} selesai dalam {ms:.2f} ms"
        if detail:
            status_teks += f" | {detail}"
        self.lbl_status.config(text=status_teks)

    def jalankan_perintah(self):
        if not self.menu_terpilih:
            return
        teks, kat, aksi = self.menu_terpilih

        try:
            if aksi == "load":
                self._eksekusi_load()
            elif kat == "m1_array":
                self._eksekusi_m1(self.array_pesanan, "Array", aksi)
            elif kat == "m1_linked":
                self._eksekusi_m1(self.linklist_pesanan, "LinkList", aksi)
            elif kat == "m2_stack":
                self._eksekusi_m2_stack(aksi)
            elif kat == "m2_queue":
                self._eksekusi_m2_queue(aksi)
            elif kat == "m3_sort":
                self._eksekusi_m3_sort(aksi)
            elif kat == "m3_search":
                self._eksekusi_m3_search(aksi)

        except ValueError as ve:
            self.tulis_hasil(f"[GALAT NILAI] {str(ve)}")
        except IndexError as ie:
            self.tulis_hasil(f"[GALAT INDEKS] {str(ie)}")
        except FileNotFoundError:
            self.tulis_hasil(f"[GALAT] Berkas tidak ditemukan:\n{CSV_PATH}")
        except Exception as e:
            self.tulis_hasil(f"[GALAT TAK TERDUGA] {type(e).__name__}: {str(e)}")

    # -----------------------------------------------------------------------
    # Eksekutor Menu DATA
    # -----------------------------------------------------------------------
    def _eksekusi_load(self):
        if not os.path.exists(CSV_PATH):
            self.tulis_hasil(f"Berkas data tidak ditemukan pada alamat:\n{CSV_PATH}")
            return

        self.tulis_hasil("Sedang membaca data dari CSV, mohon tunggu sebentar...")
        self.root.update_idletasks()

        # Baca data CSV
        data_pesanan, ms_baca = ukur(muat_pesanan_csv, CSV_PATH)
        self.raw_data = data_pesanan

        # Muat ke Array & LinkList
        def _muat_semua():
            arr = Array(initial_capacity=len(data_pesanan) + 8)
            ll = LinkList()
            for p in data_pesanan:
                arr.append(p)
                ll.append(p)
            return (arr, ll)

        (arr, ll), ms_muat = ukur(_muat_semua)
        self.array_pesanan = arr
        self.linklist_pesanan = ll

        # Inisialisasi antrean untuk M2
        _, ms_antrean = ukur(self.antrean_manager.muat_dari_list, data_pesanan)
        self.daftar_terurut_oid = None # Reset cache pencarian

        info = (
            f"BERHASIL MEMUAT DATA\n"
            f"========================================================\n"
            f"Lokasi Berkas  : {CSV_PATH}\n"
            f"Total Baris    : {len(data_pesanan):,} pesanan\n"
            f"Waktu Baca CSV : {ms_baca:.2f} ms\n"
            f"Waktu Struktur : {ms_muat:.2f} ms (Array & LinkList)\n"
            f"Antrean M2     : {len(self.antrean_manager.circular):,} pesanan berstatus ANTRE\n"
            f"========================================================\n"
            f"Kapasitas Array: {self.array_pesanan.cap:,}\n"
            f"Ukuran LinkList: {len(self.linklist_pesanan):,}\n"
        )
        self.tulis_hasil(info)
        self.catat_command("load_csv", "DATA", ms_baca + ms_muat, f"{len(data_pesanan)} baris")

    # -----------------------------------------------------------------------
    # Eksekutor M1: Array & LinkList
    # -----------------------------------------------------------------------
    def _eksekusi_m1(self, struktur, nama_struktur, aksi):
        if len(struktur) == 0:
            self.tulis_hasil("Perhatian: Data masih kosong. Silakan muat data terlebih dahulu lewat menu DATA - Load CSV.")
            return

        if aksi == "lihat":
            teks_input = self.entry_param1.get().strip()
            if not teks_input.isdigit():
                raise ValueError("Masukkan nomor urut (indeks) yang berupa bilangan bulat positif.")
            idx = int(teks_input)
            item, ms = ukur(struktur.get, idx)
            info = (
                f"DETAIL PESANAN KE-{idx} PADA {nama_struktur.upper()}\n"
                f"========================================================\n"
                f"{item.to_display_string()}\n"
                f"========================================================\n"
                f"Total elemen di {nama_struktur}: {len(struktur):,}"
            )
            self.tulis_hasil(info)
            self.catat_command(f"lihat_pesanan[{idx}]", f"M1 - {nama_struktur}", ms)

        elif aksi in ("tambah_reguler", "tambah_prioritas", "tambah_vip"):
            nama = self.entry_param1.get().strip() or "Pelanggan Baru"
            oid = f"O-{self.no_baru:06d}"
            self.no_baru += 1

            prio = 3
            if aksi == "tambah_vip":
                prio = 1
            elif aksi == "tambah_prioritas":
                prio = 2

            pesanan_baru = Pesanan(
                oid=oid, pelanggan=nama, resto="kafe-teknik", menu="roti-bakar",
                harga=15000, prioritas=prio, t_masuk_detik=30000,
                t_selesai_detik=None, status="ANTRE"
            )

            pos, ms = ukur(tambah_pesanan, struktur, pesanan_baru)
            info = (
                f"BERHASIL MENAMBAHKAN PESANAN KE {nama_struktur.upper()}\n"
                f"========================================================\n"
                f"Posisi Indeks  : Disisipkan pada indeks ke-{pos}\n"
                f"Prioritas      : {pesanan_baru.label_prioritas()}\n"
                f"ID Pesanan     : {pesanan_baru.oid}\n"
                f"Pelanggan      : {pesanan_baru.pelanggan}\n"
                f"Total Pesanan  : {len(struktur):,} elemen\n"
                f"========================================================\n"
            )
            self.tulis_hasil(info)
            self.catat_command(aksi, f"M1 - {nama_struktur}", ms, f"Posisi {pos}")

        elif aksi == "hapus":
            teks_input = self.entry_param1.get().strip()
            if not teks_input.isdigit():
                raise ValueError("Masukkan nomor urut (indeks) yang berupa bilangan bulat positif.")
            idx = int(teks_input)
            terhapus, ms = ukur(struktur.delete, idx)
            info = (
                f"BERHASIL MENGHAPUS PESANAN DARI {nama_struktur.upper()}\n"
                f"========================================================\n"
                f"Dihapus dari Posisi: Indeks ke-{idx}\n"
                f"Pesanan Terhapus   : {terhapus.oid} ({terhapus.pelanggan} - {terhapus.menu})\n"
                f"Sisa Pesanan       : {len(struktur):,} elemen\n"
                f"========================================================\n"
            )
            self.tulis_hasil(info)
            self.catat_command(f"hapus_pesanan[{idx}]", f"M1 - {nama_struktur}", ms)

    # -----------------------------------------------------------------------
    # Eksekutor M2: Stack (Postfix, Undo, Redo)
    # -----------------------------------------------------------------------
    def _eksekusi_m2_stack(self, aksi):
        if aksi == "postfix":
            ekspresi = self.entry_param1.get().strip()
            if not ekspresi:
                ekspresi = "( 3 * 12000 ) + ( 2 * 8500 ) - 5000"

            def _proses():
                tok_post, str_post, lk1 = ke_postfix(ekspresi)
                tot, lk2 = hitung(tok_post)
                return (tok_post, str_post, lk1, tot, lk2)

            (tok_post, str_post, lk1, tot, lk2), ms = ukur(_proses)

            baris = [
                f"Struk belanja (infix) : {ekspresi}",
                f"Bentuk postfix        : {str_post}",
                f"TOTAL PERHITUNGAN     : Rp {tot:,}",
                "",
                f"{'langkah':<10s} | {'token':<8s} | {'tindakan':<38s} | {'stack':<22s} | {'output'}",
                "-" * 95
            ]
            for langkah, t, act, st, out in lk1:
                baris.append(f"{langkah:<10s} | {t:<8s} | {act:<38s} | {st:<22s} | {out}")
            baris.append("-" * 95)
            for langkah, t, act, st, out in lk2:
                baris.append(f"{langkah:<10s} | {t:<8s} | {act:<38s} | {st:<22s} | {out}")

            self.tulis_hasil("\n".join(baris))
            self.catat_command("stack_postfix", "M2 - stack", ms, f"Total Rp {tot:,}")

        elif aksi == "undo":
            hasil, ms = ukur(self.antrean_manager.undo_last)
            if hasil is None:
                self.tulis_hasil("Tumpukan undo kosong. Tidak ada aksi yang dapat dibatalkan saat ini.")
                self.catat_command("stack_undo", "M2 - stack", ms, "Undo kosong")
                return

            tipe, data = hasil
            if tipe == "ENQUEUE":
                detail = f"Pembatalan enqueue: {data.oid} dikeluarkan lagi dari belakang kedua antrean."
            else:
                detail = f"Pembatalan dequeue: {len(data)} pesanan dikembalikan ke DEPAN antrean circular dan naif."

            info = (
                f"AKSI PEMBATALAN (UNDO) BERHASIL\n"
                f"========================================================\n"
                f"{detail}\n"
                f"Panjang antrean saat ini:\n"
                f"  - Antrean Naif     : {len(self.antrean_manager.naif):,} pesanan\n"
                f"  - Antrean Circular : {len(self.antrean_manager.circular):,} pesanan\n"
                f"Status tumpukan:\n"
                f"  - Undo Depth       : {len(self.antrean_manager.stack_undo)}\n"
                f"  - Redo Depth       : {len(self.antrean_manager.stack_redo)}\n"
                f"========================================================\n"
            )
            self.tulis_hasil(info)
            self.catat_command("stack_undo", "M2 - stack", ms, detail)

        elif aksi == "redo":
            hasil, ms = ukur(self.antrean_manager.redo_last)
            if hasil is None:
                self.tulis_hasil("Tumpukan redo kosong. Tidak ada aksi yang dapat diulang saat ini.")
                self.catat_command("stack_redo", "M2 - stack", ms, "Redo kosong")
                return

            tipe, data = hasil
            if tipe == "ENQUEUE":
                detail = f"Pengerjaan ulang enqueue: {data.oid} dimasukkan kembali ke belakang antrean."
            else:
                detail = f"Pengerjaan ulang dequeue: {len(data)} pesanan dikeluarkan lagi dari antrean."

            info = (
                f"AKSI PENGERJAAN ULANG (REDO) BERHASIL\n"
                f"========================================================\n"
                f"{detail}\n"
                f"Panjang antrean saat ini:\n"
                f"  - Antrean Naif     : {len(self.antrean_manager.naif):,} pesanan\n"
                f"  - Antrean Circular : {len(self.antrean_manager.circular):,} pesanan\n"
                f"Status tumpukan:\n"
                f"  - Undo Depth       : {len(self.antrean_manager.stack_undo)}\n"
                f"  - Redo Depth       : {len(self.antrean_manager.stack_redo)}\n"
                f"========================================================\n"
            )
            self.tulis_hasil(info)
            self.catat_command("stack_redo", "M2 - stack", ms, detail)

    # -----------------------------------------------------------------------
    # Eksekutor M2: Queue (Enqueue, Dequeue Naif vs Circular)
    # -----------------------------------------------------------------------
    def _eksekusi_m2_queue(self, aksi):
        if aksi == "enqueue":
            nama = self.entry_param1.get().strip() or "Pelanggan Baru"
            oid = f"O-{self.no_baru:06d}"
            self.no_baru += 1

            p = Pesanan(
                oid=oid, pelanggan=nama, resto="kafe-teknik", menu="roti-bakar",
                harga=12000, prioritas=2, t_masuk_detik=60000,
                t_selesai_detik=None, status="ANTRE"
            )

            _, ms = ukur(self.antrean_manager.enqueue, p)
            info = (
                f"{oid} masuk ke barisan paling belakang pada KEDUA antrean.\n"
                f"Panjang sekarang: naif {len(self.antrean_manager.naif):,}, circular {len(self.antrean_manager.circular):,}\n\n"
                f"Detail pesanan baru:\n"
                f"{p.to_display_string()}"
            )
            self.tulis_hasil(info)
            self.catat_command("queue_enqueue", "M2 - queue", ms, f"Masuk {oid}")

        elif aksi == "dequeue_naif":
            jml = int(self.entry_param1.get().strip() or "1")
            hasil, ms = ukur(self.antrean_manager.dequeue_naif, jml)

            geseran = self.antrean_manager.naif.geseran_terakhir
            total_g = self.antrean_manager.naif.total_geseran

            baris = [
                f"{len(hasil)} pesanan keluar dari depan antrean naif.",
                f"Total {geseran:,} elemen digeser pada operasi ini.",
                f"Sisa antrean naif: {len(self.antrean_manager.naif):,}",
                "",
                f"{'#':<4s} | {'oid':<10s} | {'pelanggan':<22s} | {'resto':<16s} | {'menu':<16s} | {'harga'}",
                "-" * 85
            ]
            for idx, p in enumerate(hasil, 1):
                baris.append(f"{idx:<4d} | {p.oid:<10s} | {p.pelanggan:<22s} | {p.resto:<16s} | {p.menu:<16s} | Rp {p.harga:,}")

            self.tulis_hasil("\n".join(baris))
            self.catat_command("queue_dequeue_naive", "M2 - queue naif", ms, f"{geseran} elemen digeser")

        elif aksi == "dequeue_circular":
            jml = int(self.entry_param1.get().strip() or "1")
            hasil, ms = ukur(self.antrean_manager.dequeue_circular, jml)

            c = self.antrean_manager.circular
            baris = [
                f"{len(hasil)} pesanan keluar dari depan antrean circular.",
                f"Tidak ada elemen yang digeser: front sekarang {c.front}, rear {c.rear}, kapasitas {c.cap:,}.",
                f"Sisa antrean circular: {len(c):,}",
                "",
                f"{'#':<4s} | {'oid':<10s} | {'pelanggan':<22s} | {'resto':<16s} | {'menu':<16s} | {'harga'}",
                "-" * 85
            ]
            for idx, p in enumerate(hasil, 1):
                baris.append(f"{idx:<4d} | {p.oid:<10s} | {p.pelanggan:<22s} | {p.resto:<16s} | {p.menu:<16s} | Rp {p.harga:,}")

            self.tulis_hasil("\n".join(baris))
            self.catat_command("queue_dequeue_circular", "M2 - queue circular", ms, "0 elemen digeser")

    # -----------------------------------------------------------------------
    # Eksekutor M3: Sort (Insertion Sort vs Merge Sort)
    # -----------------------------------------------------------------------
    def _eksekusi_m3_sort(self, aksi):
        if not self.raw_data:
            self.tulis_hasil("Data pesanan belum dimuat. Silakan jalankan menu DATA - Load CSV terlebih dahulu.")
            return

        jml_str = self.entry_param1.get().strip() or "2000"
        if not jml_str.isdigit():
            raise ValueError("Jumlah baris harus berupa bilangan bulat positif.")
        jml = int(jml_str)
        kunci = self.var_kunci.get()

        sub_data = self.raw_data[:jml]

        if aksi == "insertion_sort":
            (terurut, cmp_cnt, mov_cnt), ms = ukur(insertion_sort, list(sub_data), kunci)
            alg_name = "insertion_sort"
            mod_name = "M3 - insertion sort"
        else:
            (terurut, cmp_cnt, mov_cnt), ms = ukur(merge_sort, list(sub_data), kunci)
            alg_name = "merge_sort"
            mod_name = "M3 - merge sort"

        # Format tampilan tabel hasil 15 baris pertama
        tampil_count = min(15, len(terurut))
        baris = [
            f"HASIL PENGURUTAN ({alg_name.upper()})",
            f"Jumlah baris diurutkan : {len(sub_data):,} pesanan",
            f"Kunci pengurutan       : {kunci}",
            f"Jumlah perbandingan    : {cmp_cnt:,} perbandingan",
            f"Jumlah pemindahan      : {mov_cnt:,} pemindahan",
            f"Waktu eksekusi         : {ms:.2f} ms",
            "",
            f"Menampilkan {tampil_count} baris teratas hasil pengurutan:",
            f"{'#':<4s} | {'oid':<10s} | {'harga':<10s} | {'selesai':<10s} | {'resto':<16s} | {'menu'}",
            "-" * 75
        ]
        for i in range(tampil_count):
            p = terurut[i]
            sel_str = str(p.t_selesai_detik) if p.t_selesai_detik is not None else "-"
            baris.append(f"{i+1:<4d} | {p.oid:<10s} | Rp {p.harga:<7,d} | {sel_str:<10s} | {p.resto:<16s} | {p.menu}")

        self.tulis_hasil("\n".join(baris))
        self.catat_command(alg_name, mod_name, ms, f"{cmp_cnt:,} perbandingan")

    # -----------------------------------------------------------------------
    # Eksekutor M3: Search (Linear Search vs Binary Search)
    # -----------------------------------------------------------------------
    def _eksekusi_m3_search(self, aksi):
        if not self.raw_data:
            self.tulis_hasil("Data pesanan belum dimuat. Silakan jalankan menu DATA - Load CSV terlebih dahulu.")
            return

        target_oid = self.entry_param1.get().strip()
        if not target_oid:
            raise ValueError("Nomor pesanan (oid) target tidak boleh kosong.")

        if aksi == "linear_search":
            (idx, cmp_cnt), ms = ukur(linear_search, self.raw_data, target_oid, "oid")
            if idx != -1:
                p = self.raw_data[idx]
                info = (
                    f"PENCARIAN LINEAR SEARCH BERHASIL\n"
                    f"========================================================\n"
                    f"Target OID          : {target_oid}\n"
                    f"Ditemukan di Indeks : {idx:,} (baris ke-{idx+1:,})\n"
                    f"Jumlah Perbandingan : {cmp_cnt:,} perbandingan\n"
                    f"Waktu Eksekusi      : {ms:.2f} ms\n"
                    f"========================================================\n"
                    f"Detail Pesanan:\n"
                    f"{p.to_display_string()}"
                )
            else:
                info = f"Pesanan {target_oid} TIDAK DITEMUKAN setelah {cmp_cnt:,} perbandingan ({ms:.2f} ms)."

            self.tulis_hasil(info)
            self.catat_command("linear_search", "M3 - linear", ms, f"{cmp_cnt:,} perbandingan")

        elif aksi == "binary_search":
            # Binary search butuh data terurut menurut OID
            ms_sort = 0.0
            if self.daftar_terurut_oid is None:
                (self.daftar_terurut_oid, _, _), ms_sort = ukur(merge_sort, list(self.raw_data), "oid")

            (idx, cmp_cnt), ms = ukur(binary_search, self.daftar_terurut_oid, target_oid, "oid")

            if idx != -1:
                p = self.daftar_terurut_oid[idx]
                baris_sort = f"Daftar terurut oid dibangun sekali dengan merge sort: {ms_sort:.2f} ms\n" if ms_sort > 0 else "Menggunakan indeks daftar terurut oid dari memori.\n"
                info = (
                    f"PENCARIAN BINARY SEARCH BERHASIL\n"
                    f"========================================================\n"
                    f"{baris_sort}"
                    f"Target OID          : {target_oid}\n"
                    f"Ditemukan di Indeks : {idx:,} (baris ke-{idx+1:,})\n"
                    f"Jumlah Perbandingan : {cmp_cnt} perbandingan\n"
                    f"Waktu Eksekusi      : {ms:.2f} ms\n"
                    f"========================================================\n"
                    f"Detail Pesanan:\n"
                    f"{p.to_display_string()}"
                )
            else:
                info = f"Pesanan {target_oid} TIDAK DITEMUKAN setelah {cmp_cnt} perbandingan ({ms:.2f} ms)."

            self.tulis_hasil(info)
            self.catat_command("binary_search", "M3 - binary", ms, f"{cmp_cnt} perbandingan")


# Alias kelas untuk kompatibilitas
Aplikasi = AppUI