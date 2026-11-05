# Solar Power Generation Dashboard

## Deskripsi Proyek

**Solar Power Generation Dashboard** merupakan aplikasi visualisasi data interaktif yang dikembangkan menggunakan Python dan Streamlit. Proyek ini berfokus pada analisis performa pembangkit listrik tenaga surya berdasarkan data produksi energi dan kondisi lingkungan.

Dashboard menyajikan informasi mengenai estimasi energi yang dihasilkan, rata-rata AC Power, rata-rata Irradiation, serta jumlah observasi. Pengguna juga dapat membandingkan performa dua pembangkit listrik melalui berbagai visualisasi interaktif.

Proyek ini mencakup tahapan pengumpulan data, pembersihan data, penggabungan dataset, eksplorasi data, analisis, dan pengembangan dashboard.

## Identitas Pengembang

- **Nama:** Raka Ramadhan
- **NIM:** 241051016
- **Program Studi:** Sistem Informasi
- **Mata Kuliah:** Visualisasi Data
- **Dosen Pengampu:** Muryan Awaludin, S.Kom., M.Kom.

## Dashboard dan Repository

| Keterangan | Tautan |
|---|---|
| Live Dashboard | https://uts-visualisasi-data-solar.streamlit.app/ |
| GitHub Repository | https://github.com/Dakaa69/UTS-Visualisasi-Data-Solar |

## Sumber Dataset

Dataset yang digunakan dalam proyek ini adalah **Solar Power Generation Data** yang dipublikasikan oleh Ani Kannal melalui Kaggle.

Dataset tersebut berisi informasi produksi listrik dan kondisi lingkungan dari dua pembangkit listrik tenaga surya.

**Informasi dataset:**

- Periode pengamatan: 15 Mei 2020 sampai 17 Juni 2020.
- Jumlah observasi setelah penggabungan: 136.476 baris.
- Jumlah pembangkit: 2 unit.
- Data produksi: DC Power, AC Power, Daily Yield, dan Total Yield.
- Data lingkungan: Ambient Temperature, Module Temperature, dan Irradiation.

**Tautan Dataset:**

https://www.kaggle.com/datasets/anikannal/solar-power-generation-data

## Teknologi yang Digunakan

| Teknologi | Kegunaan |
|---|---|
| Python | Bahasa pemrograman utama |
| Streamlit | Pengembangan aplikasi dashboard |
| Pandas | Pembersihan dan pengolahan data |
| NumPy | Operasi numerik dan perhitungan |
| Plotly | Pembuatan visualisasi interaktif |
| JupyterLab | Eksplorasi dan analisis data |

## Fitur Dashboard

Dashboard menyediakan beberapa fitur utama untuk membantu pengguna memahami performa pembangkit listrik tenaga surya.

1. **Control Panel**  
   Menyediakan filter berdasarkan pembangkit dan rentang tanggal.

2. **Overview Performa**  
   Menampilkan empat indikator utama:
   - Estimated Energy
   - Average AC Power
   - Average Irradiation
   - Total Records

3. **Analisis Temporal**  
   Menampilkan tren estimasi energi harian untuk mengamati perubahan produksi energi selama periode pengamatan.

4. **Pola Intrahari**  
   Menampilkan rata-rata AC Power berdasarkan jam untuk mengidentifikasi pola produksi listrik sepanjang hari.

5. **Hubungan Antarvariabel**  
   Menampilkan hubungan antara Irradiation dan AC Power melalui visualisasi interaktif.

6. **Perbandingan Unit**  
   Menampilkan 10 inverter dengan rata-rata AC Power tertinggi berdasarkan data yang dipilih.

7. **Temuan Utama**  
   Menyajikan ringkasan analisis secara otomatis berdasarkan hasil filter pengguna.

8. **Informasi Dataset**  
   Menyediakan informasi dataset dan metodologi pengolahan data.

## Metodologi Pengolahan Data

Pengolahan data dilakukan melalui beberapa tahapan berikut:

1. **Data Collection**  
   Mengumpulkan data produksi energi dan kondisi lingkungan dari dataset Kaggle.

2. **Data Cleaning**  
   Memeriksa tipe data, nilai kosong, duplikasi, dan konsistensi timestamp.

3. **Data Integration**  
   Menggabungkan data pembangkitan listrik dan data cuaca dari Plant 1 dan Plant 2 berdasarkan timestamp.

4. **Feature Engineering**  
   Membentuk variabel tambahan seperti tanggal, tahun, bulan, jam, nama hari, perbedaan temperatur, dan perbedaan daya.

5. **Exploratory Data Analysis (EDA)**  
   Melakukan eksplorasi untuk memahami distribusi data, pola produksi energi, dan hubungan antarvariabel.

6. **Data Visualization**  
   Menyajikan hasil analisis melalui dashboard interaktif menggunakan Streamlit dan Plotly.

## Struktur Proyek

```text
UTS-Visualisasi-Data-Solar/
│
├── data_raw/
│
├── dataset/
│   └── solar_cleaned.csv
│
├── notebooks/
│   └── EDA_Solar.ipynb
│
├── app.py
├── README.md
├── requirements.txt
└── .gitignore
```

## Instalasi dan Menjalankan Aplikasi

Ikuti langkah berikut untuk menjalankan aplikasi pada komputer lokal.

### 1. Clone Repository

```bash
git clone https://github.com/Dakaa69/UTS-Visualisasi-Data-Solar.git
```

### 2. Masuk ke Folder Proyek

```bash
cd UTS-Visualisasi-Data-Solar
```

### 3. Instalasi Library

```bash
py -m pip install -r requirements.txt
```

### 4. Jalankan Aplikasi

```bash
py -m streamlit run app.py
```

Setelah aplikasi berhasil dijalankan, Streamlit akan memberikan alamat lokal yang dapat dibuka melalui browser.

## Catatan Analisis

Estimasi energi dihitung berdasarkan pasangan observasi AC Power yang berurutan dengan interval waktu 15 menit. Hasil perhitungan bergantung pada asumsi interval waktu dan satuan AC Power yang digunakan.

Analisis hubungan antara Irradiation dan AC Power digunakan untuk melihat pola keterkaitan kedua variabel. Hasil analisis bersifat deskriptif dan tidak secara langsung membuktikan hubungan sebab-akibat.

Nilai indikator dan visualisasi pada dashboard dapat berubah sesuai dengan pilihan filter pembangkit dan rentang tanggal.

## Tujuan Proyek

Proyek ini dikembangkan sebagai bagian dari Ujian Tengah Semester (UTS) mata kuliah Visualisasi Data. Tujuannya adalah menerapkan konsep pengolahan data, eksplorasi data, analisis, dan visualisasi interaktif menggunakan Python.

Melalui proyek ini, proses analisis data produksi energi surya disajikan dalam bentuk dashboard yang informatif dan mudah digunakan.

## Referensi Dataset

- **Judul:** Solar Power Generation Data
- **Pembuat:** Ani Kannal
- **Platform:** Kaggle
- **Tautan:** https://www.kaggle.com/datasets/anikannal/solar-power-generation-data

---

**Solar Power Generation Dashboard**  
Developed by **Raka Ramadhan**  
NIM: 241051016  
Program Studi Sistem Informasi  
Mata Kuliah Visualisasi Data
