import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from src.visualisasi.daftar_tabel import get_cached_data, DISPLAY_COLUMNS

# Fungsi ambil dan normalisasi data

def get_linegraph_data():
    """
    Ambil dan normalisasi data untuk line graph tren kunjungan harian.
    Pastikan kolom 'Tanggal Registrasi' ada dan bertipe datetime.
    """
    df = get_cached_data()  # Ambil data dari cache pipeline utama
    if df is None or df.empty:
        return None
    # Normalisasi nama kolom agar konsisten dengan pipeline
    col_map = {c: c for c in df.columns}
    for col in DISPLAY_COLUMNS:
        if col not in df.columns:
            for c in df.columns:
                if c.lower().replace(' ', '') == col.lower().replace(' ', ''):
                    col_map[c] = col
    df = df.rename(columns=col_map)
    # Pastikan kolom yang dibutuhkan ada
    if 'Tanggal Registrasi' not in df.columns:
        # Tampilkan warning beserta daftar kolom jika kolom tidak ditemukan
        st.warning(f"Kolom 'Tanggal Registrasi' tidak ditemukan di data. Kolom yang tersedia: {list(df.columns)}")
        return None
    # Konversi ke datetime, auto-detect format agar toleran
    df['Tanggal Registrasi'] = pd.to_datetime(df['Tanggal Registrasi'], errors='coerce')
    # Jika parsing gagal seluruhnya, tampilkan warning
    if df['Tanggal Registrasi'].isna().all():
        st.warning("Semua data pada kolom 'Tanggal Registrasi' gagal diparse ke datetime. Cek format tanggal di cache!")
        return None
    df = df.dropna(subset=['Tanggal Registrasi'])
    return df

# Komponen visualisasi line graph

def render_line_graph():
    """
    Komponen visualisasi line graph tren kunjungan harian.
    Menampilkan jumlah kunjungan per hari dengan filter interaktif (khusus Januari 2024).
    """
    st.subheader("Visualisasi: Tren Kunjungan Harian (Line Graph)")
    st.markdown("""
    <div style='color:#228B22;font-size:1.05rem;margin-bottom:0.5rem;'>
        Grafik ini menampilkan jumlah kunjungan pasien rawat jalan per hari. Gunakan filter di bawah untuk memilih rentang tanggal di bulan Januari 2024.
    </div>
    """, unsafe_allow_html=True)
    df = get_linegraph_data()  # Ambil dan normalisasi data
    if df is None or df.empty:
        st.warning("Data tidak tersedia atau kolom penting tidak ditemukan.")
        return
    # Filter hanya bulan Januari tahun 2024
    df_jan_2024 = df[(df['Tanggal Registrasi'].dt.month == 1) & (df['Tanggal Registrasi'].dt.year == 2024)].copy()
    if df_jan_2024.empty:
        st.info("Tidak ada data kunjungan pada bulan Januari 2024.")
        return
    # Tambahkan kolom hari di bulan (1-31) untuk filter slider
    df_jan_2024['Hari'] = df_jan_2024['Tanggal Registrasi'].dt.day
    # Force slider selalu mulai dari 1 sampai 30
    min_hari = 1
    max_hari = 30
    # Slider filter tanggal di bulan Januari 2024
    hari_range = st.slider(
        "Filter tanggal di bulan Januari 2024:",
        min_value=1,
        max_value=30,
        value=(min_hari, max_hari),
        step=1,
        key="filter_tanggal_jan_linegraph"
    )
    hari_awal, hari_akhir = hari_range
    # Filter data sesuai tanggal di bulan Januari 2024
    mask = (df_jan_2024['Hari'] >= hari_awal) & (df_jan_2024['Hari'] <= hari_akhir)
    df_jan_2024 = df_jan_2024[mask]
    if df_jan_2024.empty:
        st.info("Tidak ada data kunjungan untuk rentang tanggal ini di Januari 2024.")
        return
    # Agregasi jumlah kunjungan per hari di Januari 2024
    data_harian = df_jan_2024.groupby('Hari').size().reindex(range(hari_awal, hari_akhir+1), fill_value=0).reset_index(name='jumlah_kunjungan')
    # Plot line graph
    fig, ax = plt.subplots(figsize=(9, 4))
    ax.plot(data_harian['Hari'], data_harian['jumlah_kunjungan'], marker='o', color='#228B22', linewidth=2)
    ax.set_xlabel('Tanggal di Bulan Januari 2024', fontsize=11, fontweight='bold')
    ax.set_ylabel('Jumlah Kunjungan', fontsize=11, fontweight='bold')
    ax.set_title(f'Tren Kunjungan Harian Rawat Jalan RS Juliana (Januari 2024, Tanggal {hari_awal}-{hari_akhir})', fontsize=15, color="#228B22", fontweight="bold")
    ax.grid(True, linestyle='--', alpha=0.3)
    plt.xticks(data_harian['Hari'])
    plt.tight_layout()
    st.pyplot(fig)
