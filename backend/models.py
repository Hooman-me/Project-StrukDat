# backend/models.py

class Pesanan:
#inisiasi pesanan, masukin data, buang strip
    def __init__(self, oid, pelanggan, resto, menu, harga, prioritas, t_masuk_detik, t_selesai_detik, status):
        self.oid = str(oid).strip()
        self.pelanggan = str(pelanggan).strip()
        self.resto = str(resto).strip()
        self.menu = str(menu).strip()
        
        #pengaman kalo ada yang eror, kalo ga eror ubah teks jadi angka,dll
        try:
            self.harga = int(harga)
        except (ValueError, TypeError):
            self.harga = 0

        try:
            self.prioritas = int(prioritas)
        except (ValueError, TypeError):
            self.prioritas = 3

        try:
            self.t_masuk_detik = int(t_masuk_detik)
        except (ValueError, TypeError):
            self.t_masuk_detik = 0

        if t_selesai_detik is not None and str(t_selesai_detik).strip() != "":
            try:
                self.t_selesai_detik = int(t_selesai_detik)
            except (ValueError, TypeError):
                self.t_selesai_detik = None
        else:
            self.t_selesai_detik = None

        self.status = str(status).strip()

    def label_prioritas(self):
        if self.prioritas == 1:
            return "1 (VIP)"
        elif self.prioritas == 2:
            return "2 (Prioritas)"
        else:
            return "3 (Reguler)"

    def to_tuple(self):
        return (
            self.oid,
            self.pelanggan,
            self.resto,
            self.menu,
            self.harga,
            self.prioritas,
            self.t_masuk_detik,
            self.t_selesai_detik,
            self.status
        )

    def to_display_string(self):
        t_selesai_str = str(self.t_selesai_detik) if self.t_selesai_detik is not None else "-"
        return (
            f"ID Pesanan    : {self.oid}\n"
            f"Pelanggan     : {self.pelanggan}\n"
            f"Restoran      : {self.resto}\n"
            f"Menu          : {self.menu}\n"
            f"Harga         : Rp {self.harga:,}\n"
            f"Prioritas     : {self.label_prioritas()}\n"
            f"Waktu Masuk   : {self.t_masuk_detik} dtk\n"
            f"Waktu Selesai : {t_selesai_str} dtk\n"
            f"Status        : {self.status}"
        )

    def __repr__(self):
        return (
            f"Pesanan(oid='{self.oid}', pelanggan='{self.pelanggan}', "
            f"resto='{self.resto}', menu='{self.menu}', harga={self.harga}, "
            f"prioritas={self.prioritas}, status='{self.status}')"
        )
