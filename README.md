# Queens LinkedIn Problem Solver

Solusi untuk permainan **Queens LinkedIn** menggunakan algoritma **Brute Force Exhaustive Search dengan Backtracking**. Program menempatkan N ratu pada papan N×N sedemikian sehingga tidak ada dua ratu yang berada di baris, kolom, region warna yang sama, maupun bertetangga satu sama lain (termasuk diagonal).

---

## Deskripsi Program

Program membaca papan permainan dari file teks, lalu secara rekursif mencoba menempatkan ratu baris per baris. Setiap kali sebuah posisi dicoba, dilakukan validasi terhadap tiga aturan:
- Tidak ada ratu lain di baris atau kolom yang sama.
- Tidak ada ratu lain di region warna yang sama.
- Tidak ada ratu lain yang bertetangga (vertikal, horizontal, maupun diagonal).

Jika validasi gagal, algoritma melakukan *backtracking* dan mencoba kolom berikutnya. Program tersedia dalam dua mode: **CLI** dan **GUI**.

---

## Requirements

- **Python 3.10+**
- Library yang diperlukan:
  - `Pillow` — untuk menyimpan solusi sebagai gambar PNG
  - `tkinter` — untuk GUI (biasanya sudah termasuk dalam instalasi Python standar)

Install dependensi dengan perintah:

```bash
pip install Pillow
```

> **Catatan:** Untuk fitur simpan gambar, pastikan font `seguisym.ttf` (Segoe UI Symbol) tersedia di direktori yang sama dengan program, atau sudah terinstal di sistem (tersedia secara default di Windows).

---

---

## Format Input

File input berupa file `.txt` dengan format papan N×N, di mana setiap karakter merepresentasikan satu region warna. Contoh:

```
AAABB
AACBB
CCCDD
CCDDD
EEEEE
```

---

## Cara Menjalankan Program

Jalankan program dari terminal dengan perintah:

```bash
python main.py
```

Program akan menampilkan menu pemilihan mode:

```
--- Brute Force Algorithm for Queens Linkedin Problem ---

Select mode:
1. CLI Mode (Command Line Interface)
2. GUI Mode (Graphical User Interface)

Your choice (1/2):
```

### Mode CLI
Pilih `1`, lalu masukkan nama/path file input saat diminta. Setelah solusi ditemukan, program akan menampilkan papan solusi, waktu eksekusi, dan jumlah kasus yang diperiksa. Pengguna kemudian dapat memilih untuk menyimpan solusi sebagai file `.txt` dan/atau gambar `.png`.

### Mode GUI
Pilih `2`, lalu pilih file input melalui dialog file yang muncul. Klik tombol **Start** untuk memulai pencarian solusi. Visualisasi proses backtracking akan ditampilkan secara real-time. Setelah selesai:
- Tombol **Save Image** — menyimpan solusi sebagai file PNG.
- Tombol **Save Text** — menyimpan solusi sebagai file TXT.

---

## Contoh Output

| Test | Ukuran Board | Waktu Eksekusi | Kasus Diperiksa |
|------|-------------|----------------|-----------------|
| Test 1 | 9×9 | 423.64 ms | 7659 |
| Test 2 | 5×5 | 3.01 ms | 25 |
| Test 3 | 8×8 | 13.03 ms | 132 |
| Test 4 | 7×7 | 4.00 ms | 49 |
| Test 5 | 6×6 | 2.14 ms | 21 |

---

## Author

| Nama | NIM |
|------|-----|
| Beni Lesmana | 10122043 |
