# backend/bench_m1.py

import time
import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from backend.m1_pesanan import muat_pesanan_csv, Array, LinkList
from backend.models import Pesanan


def run_benchmark():
    csv_path = os.path.join(parent_dir, "data", "pesanan.csv")
    print(f"[*] Memulai pengujian benchmark pada file: {csv_path}")

    # 1. Pemuatan Data 200.000 baris
    t0 = time.perf_counter()
    arr, ll = muat_pesanan_csv(csv_path)
    t_load = (time.perf_counter() - t0) * 1000.0
    print(f"[+] Selesai memuat {len(arr)} data ke Array & LinkList dalam {t_load:.2f} ms")

    target_idx = len(arr) // 2

    sample_order = Pesanan("O-999999", "Penguji Benchmark", "resto-uji", "nasi-goreng", 25000, 1, 80000, None, "ANTRE")

    # 2. Lihat Pesanan ke-i (tengah)
    # Array: O(1)
    t0 = time.perf_counter_ns()
    item_arr = arr.get(target_idx)
    t_lihat_arr = (time.perf_counter_ns() - t0) / 1_000_000.0

    # LinkList: O(n)
    t0 = time.perf_counter_ns()
    item_ll = ll.get(target_idx)
    t_lihat_ll = (time.perf_counter_ns() - t0) / 1_000_000.0

    print(f"\n--- 1. LIHAT PESANAN KE-{target_idx} ---")
    print(f"  Array      : {t_lihat_arr:.4f} ms  (Teori O(1))")
    print(f"  LinkList   : {t_lihat_ll:.4f} ms  (Teori O(n))")

    # 3. Tambah REGULER (Ujung Belakang)
    # Array: Amortized O(1)
    t0 = time.perf_counter_ns()
    arr.append(sample_order)
    t_reg_arr = (time.perf_counter_ns() - t0) / 1_000_000.0

    # LinkList: O(1)
    t0 = time.perf_counter_ns()
    ll.append(sample_order)
    t_reg_ll = (time.perf_counter_ns() - t0) / 1_000_000.0

    print(f"\n--- 2. TAMBAH PESANAN REGULER (BELAKANG) ---")
    print(f"  Array      : {t_reg_arr:.4f} ms  (Teori O(1) amortized)")
    print(f"  LinkList   : {t_reg_ll:.4f} ms  (Teori O(1) tail)")

    # 4. Tambah PRIORITAS (Tengah)
    # Array: O(n)
    t0 = time.perf_counter_ns()
    arr.insert_prioritas(sample_order)
    t_prio_arr = (time.perf_counter_ns() - t0) / 1_000_000.0

    # LinkList: O(n)
    t0 = time.perf_counter_ns()
    ll.insert_prioritas(sample_order)
    t_prio_ll = (time.perf_counter_ns() - t0) / 1_000_000.0

    print(f"\n--- 3. TAMBAH PESANAN PRIORITAS (TENGAH) ---")
    print(f"  Array      : {t_prio_arr:.4f} ms  (Teori O(n) geser separuh elemen)")
    print(f"  LinkList   : {t_prio_ll:.4f} ms  (Teori O(n) telusur separuh rantai)")

    # 5. Tambah VIP (Paling Depan / Indeks 0)
    # Array: O(n) geser seluruh elemen
    t0 = time.perf_counter_ns()
    arr.insert_vip(sample_order)
    t_vip_arr = (time.perf_counter_ns() - t0) / 1_000_000.0

    # LinkList: O(1) ubah head
    t0 = time.perf_counter_ns()
    ll.insert_vip(sample_order)
    t_vip_ll = (time.perf_counter_ns() - t0) / 1_000_000.0

    print(f"\n--- 4. TAMBAH PESANAN VIP (PALING DEPAN) ---")
    print(f"  Array      : {t_vip_arr:.4f} ms  (Teori O(n) geser seluruh elemen)")
    print(f"  LinkList   : {t_vip_ll:.4f} ms  (Teori O(1) ubah head)")

    # 6. Hapus Pesanan ke-i (tengah)
    # Array: O(n)
    t0 = time.perf_counter_ns()
    del_arr = arr.delete(target_idx)
    t_del_arr = (time.perf_counter_ns() - t0) / 1_000_000.0

    # LinkList: O(n)
    t0 = time.perf_counter_ns()
    del_ll = ll.delete(target_idx)
    t_del_ll = (time.perf_counter_ns() - t0) / 1_000_000.0

    print(f"\n--- 5. HAPUS PESANAN KE-{target_idx} ---")
    print(f"  Array      : {t_del_arr:.4f} ms  (Teori O(n) geser kiri)")
    print(f"  LinkList   : {t_del_ll:.4f} ms  (Teori O(n) telusur ke i-1)")

    print("\n========================================================")
    print("Ringkasan Hasil Benchmark (ms):")
    print(f"{'Operasi':<20} | {'Array':<12} | {'LinkList':<12}")
    print("-" * 50)
    print(f"{'Lihat Pesanan':<20} | {t_lihat_arr:>8.4f} ms | {t_lihat_ll:>8.4f} ms")
    print(f"{'Tambah REGULER':<20} | {t_reg_arr:>8.4f} ms | {t_reg_ll:>8.4f} ms")
    print(f"{'Tambah PRIORITAS':<20} | {t_prio_arr:>8.4f} ms | {t_prio_ll:>8.4f} ms")
    print(f"{'Tambah VIP':<20} | {t_vip_arr:>8.4f} ms | {t_vip_ll:>8.4f} ms")
    print(f"{'Hapus Pesanan':<20} | {t_del_arr:>8.4f} ms | {t_del_ll:>8.4f} ms")
    print("========================================================")


if __name__ == "__main__":
    run_benchmark()
