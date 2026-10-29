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


if __name__ == "__main__":
    init_db()
    AplikasiDiabetes().mainloop()
