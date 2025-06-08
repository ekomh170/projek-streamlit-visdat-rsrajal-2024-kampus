import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from src.visualisasi.daftar_tabel import get_cached_data, DISPLAY_COLUMNS

def render_heatmap():
    """
    Visualisasi heatmap distribusi kunjungan berdasarkan hari (Senin-Minggu) dan poli.
    Menampilkan jumlah kunjungan pada setiap kombinasi hari dan poli di bulan Januari 2024.
    """
    st.subheader("Visualisasi: Heatmap Distribusi Hari & Poli (Januari 2024)")
    st.markdown("""
    <div style='background:#f1f8e9;padding:0.9rem 1.2rem 0.9rem 1.2rem;border-radius:10px;margin-bottom:1.2rem;border:1px solid #c5e1a5;'>
        Heatmap ini menampilkan distribusi jumlah kunjungan pasien rawat jalan RS Juliana berdasarkan <b>hari dalam minggu</b> (Senin-Minggu) dan <b>poliklinik</b> selama Januari 2024.
    </div>
    """, unsafe_allow_html=True)
    df = get_cached_data()
    if df is None or df.empty:
        st.warning("Data tidak tersedia atau kolom penting tidak ditemukan.")
        return
    # Filter hanya bulan Januari 2024
    df = df.copy()
    # Pastikan parsing tanggal auto-detect agar tidak error
    df['Tanggal Registrasi'] = pd.to_datetime(df['Tanggal Registrasi'], errors='coerce')
    df = df[(df['Tanggal Registrasi'].dt.month == 1) & (df['Tanggal Registrasi'].dt.year == 2024)]
    if df.empty:
        st.info("Tidak ada data kunjungan pada bulan Januari 2024.")
        return
    # Ambil hari (Senin-Minggu) dan poli
    try:
        # Tampilkan hari dalam bahasa Indonesia jika memungkinkan
        df['Hari'] = df['Tanggal Registrasi'].dt.day_name(locale='id_ID')
        hari_order = ['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu', 'Minggu']
    except Exception:
        df['Hari'] = df['Tanggal Registrasi'].dt.day_name()  # fallback ke default locale (Inggris)
        hari_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    if 'Poli' not in df.columns:
        st.warning("Kolom 'Poli' tidak ditemukan di data.")
        return
    # Pivot tabel: index=Hari, columns=Poli, values=jumlah kunjungan
    heatmap_data = pd.pivot_table(df, index='Hari', columns='Poli', values='No. Reg', aggfunc='count', fill_value=0)
    # Urutkan hari secara manual (Senin-Minggu, sesuai locale)
    heatmap_data = heatmap_data.reindex(hari_order)
    # Plot heatmap
    plt.figure(figsize=(min(1.5+0.5*len(heatmap_data.columns), 12), 6))
    sns.heatmap(heatmap_data, annot=True, fmt='d', cmap='YlGnBu', linewidths=0.5, cbar_kws={'label': 'Jumlah Kunjungan'})
    plt.title('Distribusi Kunjungan per Hari dan Poli (Januari 2024)', fontsize=15, color="#228B22", fontweight="bold")
    plt.xlabel('Poli')
    plt.ylabel('Hari')
    st.pyplot(plt.gcf())
    # Setelah heatmap tampil, tambahkan penjelasan detail di bawah
    st.markdown("""
    <div style='background:#f1f8e9;padding:0.9rem 1.2rem 0.9rem 1.2rem;border-radius:10px;margin-top:1.2rem;margin-bottom:0.5rem;border:1px solid #c5e1a5;'>
        <b>Penjelasan:</b><br>
        <ul style='margin-bottom:0.2rem;'>
            <li>Setiap sel menunjukkan total kunjungan pada kombinasi hari dan poli tertentu.</li>
            <li>Warna lebih gelap menandakan volume kunjungan lebih tinggi.</li>
            <li>Insight ini membantu manajemen mengidentifikasi hari sibuk, poli dengan beban tertinggi, dan pola kunjungan mingguan untuk perencanaan jadwal dokter serta pengelolaan ruangan.</li>
        </ul>
        Gunakan heatmap ini untuk mendukung pengambilan keputusan operasional dan optimalisasi layanan rumah sakit.
    </div>
    """, unsafe_allow_html=True)

# Untuk integrasi ke visualisasi_menu.py:
# from src.visualisasi.heatmap import render_heatmap
# lalu panggil render_heatmap() sesuai menu
