"""
Aplikasi Prediksi Risiko Diabetes
Python + Tkinter + SQLite

Jalankan:  python prediksi_diabetes.py
Database 'prediksi_diabetes.db' dibuat otomatis di folder yang sama dengan skrip ini.
"""

import os
import re
import sqlite3
import tkinter as tk
from tkinter import ttk

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "prediksi_diabetes.db")

# Warna label sesuai tingkat risiko: (warna latar, warna teks)
WARNA_RISIKO = {
    "Rendah": ("#2e7d32", "white"),
    "Waspada": ("#f9a825", "black"),
    "Sedang": ("#ef6c00", "white"),
    "Tinggi": ("#c62828", "white"),
    "Sangat Tinggi": ("#6a0000", "white"),
}


# ======================================================================
# DATABASE
# ======================================================================
def init_db():
    """Membuat database dan tabel jika belum ada."""
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS pasien (
                id            INTEGER PRIMARY KEY AUTOINCREMENT,
                nama_pasien   TEXT    NOT NULL,
                usia          INTEGER NOT NULL,
                gula_darah    REAL    NOT NULL,
                bmi           REAL    NOT NULL,
                riwayat_ortu  TEXT    NOT NULL,
                hasil_prediksi TEXT   NOT NULL
            )
            """
        )


# ======================================================================
# LOGIKA PREDIKSI
# ======================================================================
def prediksi_risiko(gula, bmi, riwayat_ortu):
    """
    Menentukan tingkat risiko diabetes.

    Aturan:
    1. Gula >= 200            -> Tinggi / Sangat Tinggi
         (Sangat Tinggi bila BMI >= 30 ATAU ada riwayat orang tua)
    2. Gula 140 - 199         -> Sedang / Tinggi
         (Tinggi bila BMI >= 30 ATAU ada riwayat orang tua)
    3. Gula < 140 & BMI >= 30 -> Waspada / Sedang
         (Sedang bila ada riwayat orang tua)
    4. Gula < 140, BMI < 30, ada riwayat   -> Waspada
    5. Gula < 140, BMI < 30, tanpa riwayat -> Rendah
    """
    ada_riwayat = riwayat_ortu == "Ya"
    obesitas = bmi >= 30
    faktor_tambahan = obesitas or ada_riwayat

    if gula >= 200:
        return "Sangat Tinggi" if faktor_tambahan else "Tinggi"

    if 140 <= gula < 200:
        return "Tinggi" if faktor_tambahan else "Sedang"

    # gula < 140
    if obesitas:
        return "Sedang" if ada_riwayat else "Waspada"
    if ada_riwayat:
        return "Waspada"
    return "Rendah"


# ======================================================================
# VALIDASI INPUT
# ======================================================================
def parse_angka(teks):
    """Mengubah teks menjadi float (menerima koma atau titik sebagai desimal)."""
    return float(teks.strip().replace(",", "."))


def validasi_input(nama, usia_s, gula_s, bmi_s, riwayat):
    """Mengembalikan (data_valid, pesan_error)."""
    nama = nama.strip()
    if not nama:
        return None, "Nama pasien tidak boleh kosong."
    if len(nama) < 2 or len(nama) > 100:
        return None, "Nama pasien harus 2 - 100 karakter."
    if not re.fullmatch(r"[A-Za-z\s.'\-]+", nama):
        return None, "Nama pasien hanya boleh berisi huruf, spasi, titik, apostrof, dan tanda hubung."

    if not usia_s.strip():
        return None, "Usia tidak boleh kosong."
    if not usia_s.strip().isdigit():
        return None, "Usia harus berupa bilangan bulat positif."
    usia = int(usia_s.strip())
    if not 1 <= usia <= 120:
        return None, "Usia harus antara 1 - 120 tahun."

    try:
        gula = parse_angka(gula_s)
    except ValueError:
        return None, "Kadar gula darah harus berupa angka."
    if not 20 <= gula <= 800:
        return None, "Kadar gula darah harus antara 20 - 800 mg/dL."

    try:
        bmi = parse_angka(bmi_s)
    except ValueError:
        return None, "BMI harus berupa angka."
    if not 10 <= bmi <= 70:
        return None, "BMI harus antara 10 - 70."

    if riwayat not in ("Ya", "Tidak"):
        return None, "Pilih riwayat diabetes orang tua (Ya/Tidak)."

    return (nama, usia, gula, bmi, riwayat), None


# ======================================================================
# APLIKASI TKINTER
# ======================================================================
class AplikasiDiabetes(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Prediksi Risiko Diabetes")
        self.geometry("460x520")
        self.resizable(False, False)
        self.configure(bg="#f5f5f5")
        self._buat_widget()

    def _buat_widget(self):
        tk.Label(
            self, text="Prediksi Risiko Diabetes",
            font=("Segoe UI", 16, "bold"), bg="#f5f5f5", fg="#1a237e",
        ).pack(pady=(15, 5))
        tk.Label(
            self, text="Isi data pasien di bawah ini",
            font=("Segoe UI", 9), bg="#f5f5f5", fg="#555",
        ).pack(pady=(0, 10))

        form = tk.Frame(self, bg="#f5f5f5")
        form.pack(padx=25, fill="x")
        form.columnconfigure(1, weight=1)

        self.var_nama = tk.StringVar()
        self.var_usia = tk.StringVar()
        self.var_gula = tk.StringVar()
        self.var_bmi = tk.StringVar()
        self.var_riwayat = tk.StringVar()

        baris = [
            ("Nama Pasien", self.var_nama, None),
            ("Usia (tahun)", self.var_usia, None),
            ("Gula Darah (mg/dL)", self.var_gula, None),
            ("BMI", self.var_bmi, None),
        ]
        for i, (label, var, _) in enumerate(baris):
            tk.Label(form, text=label, bg="#f5f5f5", anchor="w",
                     font=("Segoe UI", 10)).grid(row=i, column=0, sticky="w", pady=6)
            ttk.Entry(form, textvariable=var, width=28).grid(row=i, column=1, sticky="ew", padx=(10, 0))

        tk.Label(form, text="Riwayat Diabetes Ortu", bg="#f5f5f5", anchor="w",
                 font=("Segoe UI", 10)).grid(row=4, column=0, sticky="w", pady=6)
        self.cmb_riwayat = ttk.Combobox(
            form, textvariable=self.var_riwayat, values=["Ya", "Tidak"],
            state="readonly", width=26,
        )
        self.cmb_riwayat.grid(row=4, column=1, sticky="ew", padx=(10, 0))
        self.cmb_riwayat.current(1)  # default: Tidak


if __name__ == "__main__":
    init_db()
    AplikasiDiabetes().mainloop()
