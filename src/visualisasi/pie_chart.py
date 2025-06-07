import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from src.visualisasi.daftar_tabel import get_cached_data, DISPLAY_COLUMNS

def get_piechart_data():
    """
    Ambil dan normalisasi data untuk pie chart, pastikan kolom 'JK' (jenis kelamin) dan 'Penjamin' konsisten.
    Kembalikan DataFrame dengan kolom: 'JK', 'Penjamin'.
    """
    df = get_cached_data()
    if df is None or df.empty:
        return None
    # Normalisasi nama kolom agar konsisten
    col_map = {c: c for c in df.columns}
    for col in DISPLAY_COLUMNS:
        if col not in df.columns:
            for c in df.columns:
                if c.lower().replace(' ', '') == col.lower().replace(' ', ''):
                    col_map[c] = col
    df = df.rename(columns=col_map)
    # Pastikan kolom yang dibutuhkan ada
    if not all(col in df.columns for col in ['JK', 'Penjamin']):
        st.warning("Kolom 'JK' atau 'Penjamin' tidak ditemukan di data.")
        return None
    return df

def render_pie_chart():
    """
    Komponen visualisasi pie chart interaktif di dashboard.
    Menampilkan proporsi pasien berdasarkan jenis kelamin atau penjamin.
    Tampilan responsif dan proporsional.
    """
    st.subheader("Visualisasi: Pie Chart Proporsi Pasien")
    df = get_piechart_data()
    if df is None or df.empty:
        st.warning("Data tidak tersedia atau kolom penting tidak ditemukan.")
        return
    opsi = st.radio(
        "Tampilkan proporsi berdasarkan:",
        ["Jenis Kelamin", "Penjamin"],
        key="piechart_opsi",
        horizontal=True,
        label_visibility="collapsed"
    )
    if opsi == "Jenis Kelamin":
        data = df['JK'].value_counts()
        labels = data.index
        values = data.values
        title = "Proporsi Pasien Berdasarkan Jenis Kelamin"
        colors = ["#228B22", "#DFF0D8", "#A9DFBF", "#F7DC6F"]
    else:
        data = df['Penjamin'].value_counts()
        labels = data.index
        values = data.values
        title = "Proporsi Pasien Berdasarkan Penjamin"
        colors = ["#228B22", "#DFF0D8", "#A9DFBF", "#F7DC6F", "#F1948A", "#85C1E9"]
    # Ukuran pie chart responsif: kecil di mobile, sedang di desktop
    width = 350 if st.session_state.get('is_mobile', False) else 500
    fig, ax = plt.subplots(figsize=(width/100, width/100))
    wedges, texts, autotexts = ax.pie(
        values,
        labels=labels,
        autopct="%1.1f%%",
        startangle=90,
        colors=colors[:len(labels)],
        textprops={'fontsize': 13, 'color': 'black'}
    )
    ax.set_title(title, fontsize=15, color="#228B22", fontweight="bold")
    ax.axis('equal')
    st.pyplot(fig)
