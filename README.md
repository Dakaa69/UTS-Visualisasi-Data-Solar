# Solar Power Generation Dashboard

## Deskripsi Proyek

Solar Power Generation Dashboard merupakan aplikasi visualisasi data interaktif yang dikembangkan menggunakan Streamlit. Proyek ini bertujuan menganalisis performa pembangkit listrik tenaga surya berdasarkan data produksi energi dan kondisi lingkungan.

Dashboard menyajikan informasi mengenai produksi energi, rata-rata AC Power, tingkat Irradiation, serta perbandingan performa antara dua pembangkit listrik tenaga surya.

## Identitas Pengembang

- **Nama:** Raka Ramadhan
- **NIM:** 241051016
- **Program Studi:** Sistem Informasi
- **Mata Kuliah:** Visualisasi Data

## Sumber Dataset

Dataset yang digunakan adalah **Solar Power Generation Data** dari Kaggle, yang dipublikasikan oleh Ani Kannal.

Dataset mencakup informasi produksi listrik dan kondisi lingkungan dari dua pembangkit listrik tenaga surya.

- Periode pengamatan: 15 Mei 2020 sampai 17 Juni 2020.
- Jumlah observasi setelah penggabungan data: 136.476 baris.
- Jumlah pembangkit: 2.
- Data mencakup produksi DC Power, AC Power, Daily Yield, Total Yield, temperatur, dan Irradiation.

## Teknologi yang Digunakan

- Python
- Streamlit
- Pandas
- NumPy
- Plotly
- JupyterLab

## Fitur Dashboard

1. **Control Panel:** Filter pembangkit dan rentang tanggal.
2. **Overview Performa:** Menampilkan indikator utama berupa estimasi energi, rata-rata AC Power, rata-rata Irradiation, dan jumlah observasi.
3. **Analisis Temporal:** Menampilkan tren estimasi energi harian.
4. **Pola Intrahari:** Menganalisis rata-rata AC Power berdasarkan jam.
5. **Hubungan Antarvariabel:** Menampilkan hubungan Irradiation dengan AC Power.
6. **Perbandingan Unit:** Menampilkan Top 10 inverter berdasarkan rata-rata AC Power.
7. **Temuan Utama:** Menampilkan ringkasan otomatis berdasarkan data yang difilter.
8. **Informasi Dataset:** Menyediakan informasi dan metodologi pengolahan data.

## Struktur Proyek

```text
UTS-Visualisasi-Data-Solar/
│
├── data_raw/
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

### 1. Clone Repository

```bash
git clone URL_REPOSITORY_GITHUB
```

### 2. Masuk ke Folder Proyek

```bash
cd UTS-Visualisasi-Data-Solar
```

### 3. Instalasi Library

```bash
py -m pip install -r requirements.txt
```

### 4. Jalankan Streamlit

```bash
py -m streamlit run app.py
```

Aplikasi akan berjalan melalui browser menggunakan alamat lokal yang diberikan oleh Streamlit.

## Catatan Analisis

Estimasi energi dihitung menggunakan pasangan observasi AC Power yang berurutan dengan interval waktu 15 menit. Perhitungan ini merupakan estimasi berdasarkan asumsi interval pengamatan dan satuan AC Power yang digunakan.

Hasil visualisasi bersifat deskriptif. Hubungan statistik antara Irradiation dan AC Power tidak secara langsung membuktikan hubungan sebab-akibat.

## Tujuan Proyek

Proyek ini dikembangkan sebagai bagian dari Ujian Tengah Semester (UTS) mata kuliah Visualisasi Data untuk menerapkan proses pengolahan data, eksplorasi data, analisis, dan visualisasi interaktif menggunakan Python dan Streamlit.

## Sumber Data

Dataset yang digunakan dalam proyek ini berasal dari Kaggle:

- **Judul Dataset:** Solar Power Generation Data
- **Pembuat:** Ani Kannal
- **Platform:** Kaggle
- **Tautan Dataset:** https://www.kaggle.com/datasets/anikannal/solar-power-generation-data

Data telah melalui proses pembersihan, penggabungan, dan transformasi sebelum digunakan dalam analisis serta visualisasi dashboard.