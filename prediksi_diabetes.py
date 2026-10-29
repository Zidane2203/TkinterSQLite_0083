"""
Aplikasi Prediksi Risiko Diabetes
Python + Tkinter + SQLite

Jalankan:  python prediksi_diabetes.py
Database 'prediksi_diabetes.db' dibuat otomatis di folder yang sama dengan skrip ini.
"""

import os
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


if __name__ == "__main__":
    init_db()
    AplikasiDiabetes().mainloop()
