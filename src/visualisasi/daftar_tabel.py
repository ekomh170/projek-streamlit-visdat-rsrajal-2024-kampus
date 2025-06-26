import streamlit as st
from src.data_handler.spreadsheet_connector import load_sheet_data
from math import ceil
import os
import pickle
import re

# Kolom yang ingin ditampilkan di tabel (langsung satu konstanta saja)
DISPLAY_COLUMNS = [
    "Tanggal Registrasi", "No. Reg", "No. RM Lama", "No. RM Baru",
    "Nama Pasien Anonim", "JK", "Umur / Tahun", "Poli", "Dokter", "Penjamin",
    "Petugas Anonim"
]

# Link Google Spreadsheet dan nama sheet yang dipakai
SHEET_URL = st.secrets["SHEET_URL"] if "SHEET_URL" in st.secrets else "https://docs.google.com/spreadsheets/d/1Uqg-6Zp64VCv9_1b4soV9KSkRL0WkMjbcxmXWnVxpYA/edit?usp=sharing"
WORKSHEET_NAME = st.secrets["WORKSHEET_NAME"] if "WORKSHEET_NAME" in st.secrets else "Januari"
# Lokasi file cache lokal biar loading data lebih ngebut
CACHE_PATH = "data/processed/cache_tabel_kunjungan.pkl"

def load_data():
    """
    Fungsi buat ambil data dari Google Sheets.
    Kalau gagal (misal: internet mati/Google error), coba ambil dari file lokal.
    Kalau dua-duanya gagal, kasih info error lengkap ke user.
    """
    try:
        # Ambil kredensial dari secrets jika ada, jika tidak fallback ke file lokal
        creds_path = None
        creds_json = st.secrets.get("GCP_SERVICE_ACCOUNT", None)
        if creds_json:
            creds_path = creds_json
        else:
            creds_path = "json/credentials.json"
        df = load_sheet_data(SHEET_URL, WORKSHEET_NAME, creds_path=creds_path)
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
        # Hapus kolom Diagnosa Akhir jika ada
        if "Diagnosa Akhir" in df.columns:
            df = df.drop(columns=["Diagnosa Akhir"])
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
            # Hapus kolom Diagnosa Akhir jika ada
            if "Diagnosa Akhir" in df.columns:
                df = df.drop(columns=["Diagnosa Akhir"])
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
    Nama dokter otomatis diganti alias nama manusia demi privasi.
    """
    # Normalisasi nama kolom agar cocok dengan DISPLAY_COLUMNS
    df = df.rename(columns={c: c.strip() for c in df.columns})
    col_map = {c: c for c in df.columns}
    for col in DISPLAY_COLUMNS:
        if col not in df.columns:
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

    # Alias nama dokter dengan nama manusia Indonesia, gelar tetap sesuai asli
    if "Dokter" in df_display.columns:
        import random
        import re
        nama_alias = [
            "Andi", "Budi", "Citra", "Dewi", "Eko", "Fajar", "Gita", "Hadi", "Indra", "Joko",
            "Kartika", "Lina", "Maya", "Nanda", "Oka", "Putri", "Rian", "Sari", "Tono", "Wulan"
        ]
        dokter_list = sorted(df_display["Dokter"].unique())
        random.seed(42)
        alias_map = {}
        for i, nama_asli in enumerate(dokter_list):
            # Ekstrak gelar depan (misal: dr., drg.) dan gelar belakang (misal: Sp.A, Sp.PD)
            match = re.match(r"^(drg?\.|dr\.|drh\.|dr\s|drg\s)?\s*([\w'\-]+)(.*)$", nama_asli.strip(), re.IGNORECASE)
            if match:
                gelar_depan = match.group(1) or "dr. "
                sisa = match.group(3) or ""
                gelar_belakang = ""
                # Cari gelar belakang (Sp.A, Sp.PD, dll) di sisa
                match_belakang = re.search(r"(Sp\.[\w\-]+|Sp\s*[A-Z]+|M\.\w+|drg\.|drh\.|dr\.|dr\s|drg\s)", sisa)
                if match_belakang:
                    gelar_belakang = match_belakang.group(1)
                alias_nama = nama_alias[i % len(nama_alias)]
                alias_map[nama_asli] = f"{gelar_depan.strip()} {alias_nama} {gelar_belakang.strip()}".replace("  ", " ").strip()
            else:
                # fallback: hanya ganti nama tengah/belakang
                alias_map[nama_asli] = f"dr. {nama_alias[i % len(nama_alias)]}"
        df_display["Dokter"] = df_display["Dokter"].map(alias_map)
        st.info("Nama dokter telah disamarkan, namun gelar tetap sesuai aslinya demi privasi dan kejelasan profesi. Jika butuh data asli, hubungi admin.")

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
    st.markdown("""
    <div style='background:#fff3cd;border:2px solid #ffe082;padding:1.1rem 1.5rem 1.1rem 1.5rem;border-radius:12px;margin-bottom:1.2rem;box-shadow:0 2px 12px rgba(255,193,7,0.10);font-size:1.05rem;'>
    <b>⚠️ Penting:</b> <br>
    <ul style='margin-bottom:0;'>
    <li>Refresh data dari Google Sheets <b>hanya jika data tidak bisa diambil dari cache/lokal</b> atau benar-benar perlu update terbaru.</li>
    <li>Jangan sering-sering refresh, karena API Google Sheets gratisan <b>ada batasan kuota</b> dan bisa menyebabkan error jika terlalu sering.</li>
    <li>Gunakan data offline/lokal jika memungkinkan untuk menghemat kuota API.</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    refresh_clicked = col1.button("🔄 Refresh Data dari Google Sheets", help="Hanya gunakan jika data tidak bisa diambil dari cache/lokal atau benar-benar perlu update terbaru. Jangan sering-sering refresh karena API Google Sheets gratisan ada batasan kuota.")
    offline_clicked = col2.button("Gunakan Data Offline (Excel Lokal)", help="Ambil data dari file lokal dan update cache")

    if refresh_clicked:
        # Konfirmasi jika data kosong/bermasalah, jika tidak bermasalah langsung refresh
        df_before = get_cached_data()
        if df_before is None or df_before.empty:
            st.warning("Data sebelumnya kosong atau bermasalah. Pastikan koneksi dan kredensial Google Sheets sudah benar sebelum refresh.\n\n<b>Jangan sering-sering refresh, gunakan hanya jika data tidak bisa diambil dari cache/lokal.</b>", unsafe_allow_html=True)
            if st.button("Tetap Lanjutkan Refresh Data?", key="force_refresh"):
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
            else:
                st.stop()
        else:
            # Ganti st.confirm dengan dialog konfirmasi manual
            if 'confirm_refresh' not in st.session_state:
                st.session_state['confirm_refresh'] = None
            if st.session_state['confirm_refresh'] is None:
                st.markdown("""
                <div style='background:#fff3cd;border:2px solid #ffe082;padding:1.2rem 1.5rem 1.2rem 1.5rem;border-radius:12px;margin-bottom:1.2rem;box-shadow:0 2px 12px rgba(255,193,7,0.10);font-size:1.1rem;'>
                <b>⚠️ Konfirmasi Refresh Data</b><br>
                Anda akan melakukan <b>refresh data dari Google Sheets</b>.<br>
                <span style='color:#b26a00;'>Tindakan ini akan menghapus cache lokal dan mengambil data terbaru dari Google Sheets.</span><br>
                <b>Pastikan koneksi dan kredensial sudah benar.</b><br>
                <span style='color:#b26a00;'><b>Jangan sering-sering refresh!</b> API Google Sheets gratisan <b>ada batasan kuota</b>. Gunakan refresh <b>hanya jika data tidak bisa diambil dari cache/lokal</b> atau benar-benar perlu update terbaru.</span><br>
                Klik <b>Konfirmasi</b> untuk melanjutkan, atau <b>Batal</b> untuk membatalkan.
                </div>
                """, unsafe_allow_html=True)
                col_confirm, col_cancel = st.columns([2,1])
                with col_confirm:
                    confirm = st.button("✅ Konfirmasi: Yakin ingin refresh data dari Google Sheets?", key="confirm_refresh_btn")
                with col_cancel:
                    cancel = st.button("❌ Batal", key="cancel_refresh_btn")
                if confirm:
                    st.session_state['confirm_refresh'] = True
                    st.experimental_rerun()
                elif cancel:
                    st.session_state['confirm_refresh'] = False
                    st.info("Refresh data dibatalkan.")
                    st.stop()
                st.stop()
            elif st.session_state['confirm_refresh']:
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
            else:
                st.info("Refresh data dibatalkan.")
                st.session_state['confirm_refresh'] = None
                st.stop()
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
            # Hapus kolom Diagnosa Akhir jika ada
            if "Diagnosa Akhir" in df.columns:
                df = df.drop(columns=["Diagnosa Akhir"])
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
