import streamlit as st
from src.data_handler.spreadsheet_connector import load_sheet_data
from math import ceil

MAIN_COLUMNS = [
    "Filter No Urut", "Tanggal Registrasi", "No. Reg", "No. RM Lama", "No. RM Baru",
    "Nama Pasien", "JK", "Umur / Tahun", "Poli", "Dokter", "Penjamin",
    "Diagnosa Akhir", "Petugas", "Nama Pasien Anonim", "Tugas Nama Pasien", "Petugas Anonim", "Tugas Petugas"
]

SHEET_URL = "https://docs.google.com/spreadsheets/d/1Uqg-6Zp64VCv9_1b4soV9KSkRL0WkMjbcxmXWnVxpYA/edit?usp=sharing"
WORKSHEET_NAME = "Januari"

def load_data():
    try:
        # Path credentials harus relatif terhadap root project (karena streamlit run main.py dari root)
        df = load_sheet_data(SHEET_URL, WORKSHEET_NAME, creds_path="json/credentials.json")
        df = df.loc[:, ~df.columns.str.match('^Unnamed|^$')]
        return df
    except Exception as e:
        st.error(f"Gagal mengambil data: {e}")
        return None

def show_paginated_table(df, page_size=50, max_rows=1000):
    df_display = df.head(max_rows)
    display_cols = [col for col in MAIN_COLUMNS if col in df_display.columns]
    df_display = df_display[display_cols]
    total_rows = len(df_display)
    total_pages = ceil(total_rows / page_size) if total_rows > 0 else 1
    if total_rows == 0:
        st.warning("Tidak ada data untuk ditampilkan.")
        return
    page = st.number_input(
        label="Halaman", min_value=1, max_value=total_pages, value=1, step=1, key="pagination"
    )
    start = (page - 1) * page_size
    end = start + page_size
    st.write(f"Menampilkan baris {start+1} - {min(end, total_rows)} dari {total_rows} (hanya {max_rows} data pertama)")
    st.dataframe(df_display.iloc[start:end])

def render_tabel_kunjungan():
    st.subheader("Tabel Data Mentah (dengan Pagination, max 1000 data)")
    df = load_data()
    if df is not None:
        show_paginated_table(df, page_size=50, max_rows=1000)
        st.info("Menampilkan maksimal 1000 data pertama untuk performa. Silakan lanjutkan ke fitur pembersihan data dan visualisasi.")
    else:
        st.warning("Data tidak tersedia. Pastikan koneksi dan kredensial sudah benar.")
