import streamlit as st
from src.data_handler.spreadsheet_connector import load_sheet_data
from math import ceil
import os
import pickle

# Kolom yang ingin ditampilkan di tabel (langsung satu konstanta saja)
DISPLAY_COLUMNS = [
    "Tanggal Registrasi", "No. Reg", "No. RM Lama", "No. RM Baru",
    "Nama Pasien Anonim", "JK", "Umur / Tahun", "Poli", "Dokter", "Penjamin",
    "Diagnosa Akhir", "Petugas Anonim"
]

# Link Google Spreadsheet dan nama sheet yang dipakai
SHEET_URL = "https://docs.google.com/spreadsheets/d/1Uqg-6Zp64VCv9_1b4soV9KSkRL0WkMjbcxmXWnVxpYA/edit?usp=sharing"
WORKSHEET_NAME = "Januari"
# Lokasi file cache lokal biar loading data lebih ngebut
CACHE_PATH = "data/processed/cache_tabel_kunjungan.pkl"

def load_data():
    """
    Fungsi buat ambil data dari Google Sheets.
    Kalau gagal (misal: internet mati/Google error), coba ambil dari file lokal.
    Kalau dua-duanya gagal, kasih info error lengkap ke user.
    """
    try:
        df = load_sheet_data(SHEET_URL, WORKSHEET_NAME, creds_path="json/credentials.json")
        df = df.loc[:, ~df.columns.str.match('^Unnamed|^$')]
        # Normalisasi nama kolom agar konsisten dengan DISPLAY_COLUMNS
        df.columns = [c.strip() for c in df.columns]
        col_map = {c: c for c in df.columns}
        for col in DISPLAY_COLUMNS:
            if col not in df.columns:
                # Coba cari kolom dengan lower-case match (toleransi typo minor)
                for c in df.columns:
                    if c.lower().replace(' ', '') == col.lower().replace(' ', ''):
                        col_map[c] = col
        df = df.rename(columns=col_map)
        return df
    except Exception as e:
        import traceback
        tb = traceback.format_exc()
        st.error(f"Gagal mengambil data dari Google Sheets.\n\nDetail error:\n{e}\n\nTraceback:\n{tb}")
        # Kalau gagal, coba ambil dari file Excel lokal
        try:
            import pandas as pd
            df = pd.read_excel("data/original/data_kunjungan_januari.xlsx")
            st.info("Data diambil dari file lokal (data/original/data_kunjungan_januari.xlsx).")
            # Normalisasi nama kolom agar konsisten dengan DISPLAY_COLUMNS
            df.columns = [c.strip() for c in df.columns]
            col_map = {c: c for c in df.columns}
            for col in DISPLAY_COLUMNS:
                if col not in df.columns:
                    # Coba cari kolom dengan lower-case match (toleransi typo minor)
                    for c in df.columns:
                        if c.lower().replace(' ', '') == col.lower().replace(' ', ''):
                            col_map[c] = col
            df = df.rename(columns=col_map)
            return df
        except Exception as e2:
            tb2 = traceback.format_exc()
            st.error(f"Gagal mengambil data lokal: {e2}\n\nTraceback:\n{tb2}")
            return None

# Fungsi ini biar data nggak ngulang loading terus, jadi lebih cepat karena disimpan di cache lokal
@st.cache_data(show_spinner=True)
def get_cached_data():
    # Cek cache Streamlit dulu, baru file lokal
    if os.path.exists(CACHE_PATH):
        try:
            with open(CACHE_PATH, "rb") as f:
                df = pickle.load(f)
            return df
        except Exception:
            pass  # Kalau cache rusak, lanjut ambil data baru
    df = load_data()
    if df is not None:
        try:
            os.makedirs(os.path.dirname(CACHE_PATH), exist_ok=True)
            with open(CACHE_PATH, "wb") as f:
                pickle.dump(df, f)
        except Exception:
            pass  # Jika gagal simpan cache, tetap lanjutkan
    return df

def show_paginated_table(df, page_size=50, max_rows=None):
    """
    Tampilkan tabel data dengan fitur pagination (bisa ganti halaman).
    Jika max_rows=None, tampilkan seluruh data.
    Hanya menampilkan kolom yang sudah disetujui user (tanpa kolom sensitif) dan urutan sesuai permintaan user.
    """
    # Normalisasi nama kolom agar cocok dengan DISPLAY_COLUMNS
    df = df.rename(columns={c: c.strip() for c in df.columns})
    col_map = {c: c for c in df.columns}
    for col in DISPLAY_COLUMNS:
        if col not in df.columns:
            # Coba cari kolom dengan lower-case match (toleransi typo minor)
            for c in df.columns:
                if c.lower().replace(' ', '') == col.lower().replace(' ', ''):
                    col_map[c] = col
    df = df.rename(columns=col_map)
    if max_rows is not None:
        df_display = df.head(max_rows).copy()
    else:
        df_display = df.copy()
    for col in DISPLAY_COLUMNS:
        if col not in df_display.columns:
            df_display[col] = ""
    df_display = df_display[DISPLAY_COLUMNS]

    total_rows = len(df_display)
    if total_rows == 0:
        st.warning("Tidak ada data untuk ditampilkan.")
        return
    total_pages = ceil(total_rows / page_size)
    page = st.number_input(
        label="Halaman", min_value=1, max_value=total_pages, value=1, step=1, key="pagination"
    )
    start = (page - 1) * page_size
    end = start + page_size
    page_df = df_display.iloc[start:end].copy()
    page_df.insert(0, "No", range(start + 1, min(end, total_rows) + 1))
    st.write(f"Menampilkan baris {start+1} - {min(end, total_rows)} dari {total_rows}")
    st.dataframe(page_df)

def render_tabel_kunjungan():
    """
    Fungsi utama buat nampilin tabel kunjungan di dashboard.
    """
    st.title("Tabel Data Mentah (dengan Pagination, max 6000 data)")
    col1, col2 = st.columns(2)
    refresh_clicked = col1.button("🔄 Refresh Data dari Google Sheets", help="Klik untuk ambil data terbaru dan reset cache")
    offline_clicked = col2.button("Gunakan Data Offline (Excel Lokal)", help="Ambil data dari file lokal dan update cache")

    if refresh_clicked:
        st.cache_data.clear()
        if os.path.exists(CACHE_PATH):
            try:
                os.remove(CACHE_PATH)
                st.success("Cache lokal berhasil dihapus. Data akan diambil ulang.")
            except Exception as e:
                st.warning(f"Gagal hapus cache lokal: {e}")
        else:
            st.info("Cache lokal tidak ditemukan, akan ambil data baru.")
        df = get_cached_data()

    elif offline_clicked:
        import pandas as pd
        try:
            df = pd.read_excel("data/original/data_kunjungan_januari.xlsx")
            st.info("Data diambil dari file lokal (data/original/data_kunjungan_januari.xlsx). Tidak menyimpan ke cache.")
            # Normalisasi nama kolom agar konsisten dengan DISPLAY_COLUMNS
            df.columns = [c.strip() for c in df.columns]
            col_map = {c: c for c in df.columns}
            for col in DISPLAY_COLUMNS:
                if col not in df.columns:
                    for c in df.columns:
                        if c.lower().replace(' ', '') == col.lower().replace(' ', ''):
                            col_map[c] = col
            df = df.rename(columns=col_map)
            # Pagination logic
            page_size = 50
            max_rows = 6000
            df_display = df.head(max_rows).copy()
            for col in DISPLAY_COLUMNS:
                if col not in df_display.columns:
                    df_display[col] = ""
            df_display = df_display[DISPLAY_COLUMNS]
            total_rows = len(df_display)
            total_pages = ceil(total_rows / page_size) if total_rows > 0 else 1
            page = st.number_input(
                label="Halaman", min_value=1, max_value=total_pages, value=1, step=1, key="pagination_offline"
            )
            start = (page - 1) * page_size
            end = start + page_size
            page_df = df_display.iloc[start:end].copy()
            page_df.insert(0, "No", range(start + 1, min(end, total_rows) + 1))
            st.write(f"Menampilkan baris {start+1} - {min(end, total_rows)} dari {total_rows} (hanya {max_rows} data pertama)")
            st.dataframe(page_df)
            if st.button("Export Data Halaman Ini ke Excel Offline", help="Tulis data halaman yang sedang tampil ke file offline tanpa validasi kolom."):
                try:
                    page_df.to_excel("data/original/data_kunjungan_januari.xlsx", index=False)
                    st.success("Data halaman ini berhasil diekspor dan menimpa file offline. Silakan refresh data offline.")
                except Exception as e:
                    st.error(f"Gagal export data ke Excel offline: {e}")
            st.info("Menampilkan maksimal 6000 data pertama untuk performa. Silakan lanjutkan ke fitur pembersihan data dan visualisasi.")
            return
        except Exception as e:
            st.error(f"Gagal mengambil data offline: {e}")
            df = None

    else:
        df = get_cached_data()

    if df is not None:
        show_paginated_table(df, page_size=50, max_rows=None)

        # Tombol export dari data online ke Excel lokal, langsung di bawah tabel
        if st.button("💾 Export Data Online ke Excel Offline", help="Ekspor seluruh data online ke file Excel lokal"):
            try:
                df.to_excel("data/original/data_kunjungan_januari.xlsx", index=False)
                st.success("Data online berhasil diekspor ke 'data/original/data_kunjungan_januari.xlsx'.")
            except Exception as e:
                st.error(f"Gagal mengekspor data: {e}")

        st.info("Menampilkan seluruh data (hingga 6000 baris) untuk performa. Silakan lanjutkan ke fitur pembersihan data dan visualisasi.")
    else:
        st.warning("Data tidak tersedia. Pastikan koneksi dan kredensial sudah benar.")
