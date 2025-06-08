import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from src.visualisasi.daftar_tabel import get_cached_data
import re

def render_scatter_plot():
    """
    Visualisasi scatter plot hubungan usia pasien dengan poli yang dikunjungi.
    Tujuan: Mengidentifikasi pola distribusi usia pasien pada masing-masing poliklinik, misal dominasi pasien anak di poli anak, lansia di poli penyakit dalam, dsb.
    """
    st.subheader("Visualisasi: Scatter Plot Usia Pasien vs Poli")
    st.markdown("""
    <div style='background:#f1f8e9;padding:0.8rem 1.2rem 0.8rem 1.2rem;border-radius:10px;margin-bottom:1.2rem;border:1px solid #c5e1a5;'>
        Scatter plot ini menampilkan sebaran usia pasien rawat jalan RS Juliana pada masing-masing poliklinik.
    </div>
    """, unsafe_allow_html=True)
    df = get_cached_data()
    if df is None or df.empty:
        st.warning("Data tidak tersedia atau kolom penting tidak ditemukan.")
        return
    # Normalisasi nama kolom agar konsisten dengan daftar_tabel
    col_map = {c.lower().replace(' ', ''): c for c in df.columns}
    usia_col = col_map.get('umur/tahun') or col_map.get('usia') or col_map.get('umur')
    poli_col = col_map.get('poli') or col_map.get('poliklinik')
    if not usia_col or not poli_col:
        st.warning(f"Kolom 'Umur / Tahun'/'Usia' dan 'Poli' tidak ditemukan di data. Kolom yang tersedia: {list(df.columns)}.\n\nCek pipeline normalisasi kolom di daftar_tabel.py dan pastikan refresh cache sudah benar.")
        return
    # Konversi usia ke numerik (jika perlu)
    def parse_usia(usia_str):
        if pd.isna(usia_str):
            return None
        usia_str = str(usia_str).strip()
        # Tangani khusus bayi baru lahir
        if usia_str in ["0 Th 0 Bln", "0Th0Bln", "0 th 0 bln", "0th0bln"]:
            return 0.01  # ~3-4 hari, agar tidak 0
        tahun = 0
        bulan = 0
        th_match = re.search(r'(\d+)\s*[Tt][Hh]', usia_str)
        bln_match = re.search(r'(\d+)\s*[Bb][Ll][Nn]', usia_str)
        if th_match:
            tahun = int(th_match.group(1))
        if bln_match:
            bulan = int(bln_match.group(1))
        if tahun == 0 and bulan == 0:
            # Coba langsung ke float
            try:
                return float(usia_str)
            except:
                return None
        return tahun + bulan/12
    
    # Terapkan parsing usia sebelum konversi numerik
    parsed_usia = df[usia_col].apply(parse_usia)
    df[usia_col + '_as_num'] = parsed_usia
    # 1. Visualisasi scatter plot
    plt.figure(figsize=(10, 5))
    sns.stripplot(data=df, x=poli_col, y=usia_col + '_as_num', jitter=True, alpha=0.7, palette='Set2')
    plt.title('Distribusi Usia Pasien pada Masing-masing Poli', fontsize=15, color="#228B22", fontweight="bold")
    plt.xlabel('Poliklinik')
    plt.ylabel('Usia Pasien')
    plt.xticks(rotation=25)
    plt.tight_layout()
    st.pyplot(plt.gcf())

    # 2. Total parsing sukses & gagal
    total_data = len(df)
    total_gagal = parsed_usia.isna().sum()
    total_sukses = total_data
    st.info(f"Total data parsing usia sukses: {total_sukses}")
    st.info(f"Total data parsing usia gagal: {total_gagal}")

    # 3. Cek problem parsing (tampilkan warning jika ada gagal parsing)
    gagal_parsing = df[parsed_usia.isna()][usia_col].unique()
    if total_gagal > 0:
        st.warning(f"Contoh data usia yang gagal parsing ({len(gagal_parsing)} unik): {gagal_parsing[:10]}")
    else:
        st.success("Tidak ada data usia yang gagal parsing.")

    # 4. Tampilkan daftar tabel hasil parsing (20 baris pertama)
    st.markdown("""
    <div style='margin-top:1.5rem;margin-bottom:0.5rem;font-weight:bold;font-size:1.1rem;'>
        Daftar Data Usia Pasien Setelah Parsing & Normalisasi
    </div>
    """, unsafe_allow_html=True)
    st.dataframe(
        df[[usia_col, usia_col + '_as_num', poli_col, 'Nama Pasien' if 'Nama Pasien' in df.columns else df.columns[0]]].head(20)
        .rename(columns={usia_col: 'Usia (Asli)', usia_col + '_as_num': 'Usia (Tahun, Desimal)', poli_col: 'Poliklinik'}),
        use_container_width=True,
        hide_index=True
    )
    st.caption('Tabel di atas menampilkan contoh data hasil parsing usia, poliklinik, dan nama pasien (maksimal 20 baris pertama). Data sudah siap untuk analisis dan visualisasi.')
    # Penjelasan insight scatter plot
    st.markdown("""
    <div style='background:#f1f8e9;padding:0.8rem 1.2rem 0.8rem 1.2rem;border-radius:10px;margin-top:1.2rem;margin-bottom:0.5rem;border:1px solid #c5e1a5;'>
        <b>Penjelasan:</b><br>
        <ul style='margin-bottom:0.2rem;'>
            <li>Setiap titik pada grafik mewakili satu pasien, posisi vertikal menunjukkan usia (tahun desimal), posisi horizontal menunjukkan poliklinik.</li>
            <li>Scatter plot memudahkan identifikasi dominasi kelompok usia tertentu pada poli tertentu (misal: anak-anak di poli anak, lansia di penyakit dalam).</li>
            <li>Insight ini membantu manajemen memahami profil demografis pasien tiap poli untuk perencanaan layanan dan strategi rumah sakit.</li>
        </ul>
        Gunakan scatter plot ini untuk mendukung analisis demografi dan perencanaan layanan berbasis data.
    </div>
    """, unsafe_allow_html=True)
    # Penjelasan singkat scatter plot dan flow data
    st.markdown("""
    <div style='background:#f1f8e9;padding:0.8rem 1rem 0.8rem 1rem;border-radius:10px;margin-top:1rem;margin-bottom:0.5rem;border:1px solid #c5e1a5;'>
    <b>Cara Kerja Scatter Plot Usia vs Poli:</b><br>
    <ol style='margin-bottom:0;'>
        <li><b>Data mentah</b> diambil dari Google Spreadsheet atau Excel, lalu diproses (cleaning dan normalisasi kolom).</li>
        <li>Kolom <b>"Umur / Tahun"</b> diparsing otomatis: format seperti <i>16 Th 4 Bln</i> diubah ke angka desimal (misal: 16.33), <i>0 Th 0 Bln</i> jadi 0.01 (bayi baru lahir).</li>
        <li>Baris yang gagal parsing usia atau poli kosong akan <b>dibuang</b> dari visualisasi (ditampilkan info debug di bawah grafik).</li>
        <li>Scatter plot menampilkan <b>setiap pasien sebagai satu titik</b>:<br>
            <ul style='margin-bottom:0;'>
                <li>Sumbu X: Nama poliklinik</li>
                <li>Sumbu Y: Usia pasien (tahun, desimal)</li>
            </ul>
        </li>
        <li>Gunakan tabel data di bawah grafik untuk melihat detail data mentah yang sudah diproses (filter, urutkan, atau ekspor ke Excel jika perlu).</li>
    </ol>
    <b>Tips:</b> Jika ada data usia yang gagal parsing, cek warning di bawah grafik untuk memperbaiki format data mentah.<br>
    </div>
    """, unsafe_allow_html=True)