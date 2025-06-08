import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from src.visualisasi.daftar_tabel import get_cached_data, DISPLAY_COLUMNS

def get_piechart_data():
    """
    Ambil dan normalisasi data untuk pie chart.
    Pastikan kolom 'JK' (jenis kelamin) dan 'Penjamin' konsisten.
    Kembalikan DataFrame dengan kolom: 'JK', 'Penjamin'.
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
    if not all(col in df.columns for col in ['JK', 'Penjamin']):
        st.warning("Kolom 'JK' atau 'Penjamin' tidak ditemukan di data.")
        return None
    return df

# Komponen utama visualisasi pie chart

def render_pie_chart():
    """
    Komponen visualisasi pie chart interaktif di dashboard.
    Menampilkan proporsi pasien berdasarkan jenis kelamin atau penjamin.
    Tampilan responsif dan proporsional.
    """
    st.subheader("Visualisasi: Pie Chart Proporsi Pasien (Januari 2024)")
    st.markdown("""
    <div style='background:#f1f8e9;padding:0.9rem 1.2rem 0.9rem 1.2rem;border-radius:10px;border:1px solid #c5e1a5;'>
        Pie chart ini menampilkan proporsi pasien rawat jalan RS Juliana berdasarkan <b>jenis kelamin</b> atau <b>penjamin</b> selama Januari 2024. Pilih kategori proporsi untuk melihat distribusi data secara visual.
    </div>
    """, unsafe_allow_html=True)
    df = get_piechart_data()
    if df is None or df.empty:
        st.warning("Data tidak tersedia atau kolom penting tidak ditemukan.")
        return
    # Pilihan proporsi: Jenis Kelamin atau Penjamin
    st.markdown("<div></div>", unsafe_allow_html=True)
    opsi = st.selectbox(
        "Tampilkan proporsi berdasarkan:",
        ["Jenis Kelamin", "Penjamin"],
        key="piechart_opsi_selectbox",
        index=0,
        help="Pilih kategori proporsi yang ingin ditampilkan"
    )
    st.markdown("<div style='margin-bottom:1.2rem;'></div>", unsafe_allow_html=True)
    # Hitung data sesuai opsi
    if opsi == "Jenis Kelamin":
        data = df['JK'].value_counts()
        labels = data.index
        values = data.values
        title = "Proporsi Pasien Berdasarkan Jenis Kelamin"
        # Warna lebih kontras dan jelas
        colors = ["#228B22", "#1976D2", "#FBC02D", "#E53935"]  # Hijau, biru, kuning, merah
        autopct_fmt = "%1.1f%%"
    else:
        data = df['Penjamin'].value_counts()
        labels = data.index
        values = data.values
        title = "Proporsi Pasien Berdasarkan Penjamin"
        # Gunakan palet tab10 dari Matplotlib agar warna kontras dan konsisten
        import matplotlib as mpl
        tab_colors = mpl.colormaps['tab10'].colors
        colors = [tab_colors[i % 10] for i in range(len(labels))]
        autopct_fmt = lambda pct: f"{pct:.1f}%\n({int(round(pct/100.*sum(values)))})"
    # Ukuran pie chart responsif: kecil di mobile, sedang di desktop
    width = 200 if st.session_state.get('is_mobile', False) else 350
    fig, ax = plt.subplots(figsize=(width/100, width/100))
    # Tampilkan pie chart tanpa label dan tanpa persentase di dalam pie, hanya legend di samping
    wedges, _ = ax.pie(
        values,
        labels=None,
        autopct=None,
        startangle=90,
        colors=colors[:len(labels)],
        textprops={'fontsize': 13, 'color': 'black'}
    )
    # Buat legend dengan label dan persentase di samping chart
    legend_title = '<b>Penjamin</b>' if opsi=='Penjamin' else '<b>Jenis Kelamin</b>'
    legend_labels = [f"{label} ({value} | {value/sum(values)*100:.1f}%)" for label, value in zip(labels, values)]
    # Render legend title dengan bold menggunakan HTML
    ax.legend(wedges, legend_labels, title=None, loc="center left", bbox_to_anchor=(1, 0.5), fontsize=12)
    # Tambahkan judul legend bold di atas chart dengan HTML (karena Matplotlib legend tidak support HTML, gunakan Streamlit)
    st.markdown(f"<div style='margin-bottom:-1.2rem;'><b>{'Penjamin' if opsi=='Penjamin' else 'Jenis Kelamin'}</b></div>", unsafe_allow_html=True)
    ax.set_title(title, fontsize=15, color="#228B22", fontweight="bold", pad=16)
    ax.axis('equal')  # Pie chart proporsional
    st.pyplot(fig)
    # Hapus deskripsi singkat duplikat di bawah diagram
    # Setelah pie chart tampil, tambahkan penjelasan detail di bawah
    st.markdown("""
    <div style='background:#DFF0D8;padding:0.8rem 1.2rem 0.8rem 1.2rem;border-radius:10px;margin-top:1.2rem;margin-bottom:0.5rem;border:1px solid #b2dfdb;'>
        <b>Penjelasan:</b><br>
        <ul style='margin-bottom:0.2rem;'>
            <li>Setiap warna pada pie chart mewakili satu kategori (jenis kelamin atau penjamin).</li>
            <li>Persentase dan jumlah pasien ditampilkan di legend samping grafik.</li>
            <li>Insight ini membantu manajemen memahami distribusi demografis pasien dan pola penjamin biaya secara cepat dan intuitif.</li>
        </ul>
        Gunakan pie chart ini untuk mendukung perencanaan layanan dan strategi rumah sakit.
    </div>
    """, unsafe_allow_html=True)
