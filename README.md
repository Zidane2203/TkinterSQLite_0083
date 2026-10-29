# Prediksi Risiko Diabetes

Aplikasi desktop sederhana untuk memprediksi risiko diabetes menggunakan
**Python**, **Tkinter**, dan **SQLite**.

> Aplikasi ini hanya alat bantu skrining sederhana, bukan pengganti diagnosis dokter.

## Fitur
- Form input: nama pasien, usia, kadar gula darah (mg/dL), BMI, dan riwayat diabetes orang tua (Combobox Ya/Tidak)
- Prediksi risiko: Rendah, Waspada, Sedang, Tinggi, Sangat Tinggi (label berwarna)
- Penyimpanan data pasien ke database SQLite `prediksi_diabetes.db`
- Tombol **Lihat Data** untuk menampilkan seluruh riwayat pasien (dengan opsi hapus data)
- Validasi input (nama, usia 1-120, gula darah 20-800, BMI 10-70)

## Cara Menjalankan
Membutuhkan Python 3.8+ (Tkinter sudah termasuk pada instalasi standar).

```bash
python prediksi_diabetes.py
```

Database dibuat otomatis di folder yang sama dengan skrip.

## Aturan Prediksi
Faktor tambahan = BMI >= 30 atau ada riwayat diabetes orang tua.

| Gula darah (mg/dL) | Kondisi | Hasil |
|---|---|---|
| >= 200 | ada faktor tambahan | Sangat Tinggi |
| >= 200 | tanpa faktor tambahan | Tinggi |
| 140 - 199 | ada faktor tambahan | Tinggi |
| 140 - 199 | tanpa faktor tambahan | Sedang |
| < 140 | BMI >= 30 dan ada riwayat | Sedang |
| < 140 | BMI >= 30 tanpa riwayat | Waspada |
| < 140 | BMI < 30 dan ada riwayat | Waspada |
| < 140 | BMI < 30 tanpa riwayat | Rendah |

## Struktur Tabel `pasien`
`id`, `nama_pasien`, `usia`, `gula_darah`, `bmi`, `riwayat_ortu`, `hasil_prediksi`
