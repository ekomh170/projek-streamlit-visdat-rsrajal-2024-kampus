import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from src.visualisasi.daftar_tabel import get_cached_data, DISPLAY_COLUMNS

def get_barchart_data():
    """
    Ambil dan normalisasi data untuk bar chart, pastikan kolom 'Poli', 'Dokter', dan 'Umur / Tahun' konsisten.
    Kembalikan DataFrame dengan kolom: 'Poli', 'Dokter', 'Umur / Tahun'.
    Kolom 'Umur / Tahun' diubah ke integer, jika gagal parsing diisi NaN.
    Nama dokter otomatis diganti alias nama manusia demi privasi.
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
    if not all(col in df.columns for col in ['Poli', 'Dokter', 'Umur / Tahun']):
        st.warning("Kolom 'Poli', 'Dokter', atau 'Umur / Tahun' tidak ditemukan di data.")
        return None
    # Konversi 'Umur / Tahun' ke integer, handle format seperti '0 Th 0 Bln'
    def parse_umur(val):
        if pd.isna(val):
            return None
        if isinstance(val, (int, float)):
            return int(val)
        # Coba ekstrak angka tahun dari string
        import re
        match = re.search(r'(\d+)\s*[Tt][Hh]', str(val))
        if match:
            return int(match.group(1))
        # Jika hanya angka
        try:
            return int(val)
        except Exception:
            return None
    df['Umur / Tahun'] = df['Umur / Tahun'].apply(parse_umur)
    df = df.dropna(subset=['Umur / Tahun'])
    # Alias nama dokter dengan nama manusia Indonesia, gelar tetap sesuai asli
    if 'Dokter' in df.columns:
        import random
        import re
        nama_alias = [
            "Andi", "Budi", "Citra", "Dewi", "Eko", "Fajar", "Gita", "Hadi", "Indra", "Joko",
            "Kartika", "Lina", "Maya", "Nanda", "Oka", "Putri", "Rian", "Sari", "Tono", "Wulan"
        ]
        dokter_list = sorted(df['Dokter'].unique())
        random.seed(42)
        alias_map = {}
        for i, nama_asli in enumerate(dokter_list):
            # Ekstrak gelar depan (misal: dr., drg.) dan gelar belakang (misal: Sp.A, Sp.PD)
            match = re.match(r"^(drg?\.|dr\.|drh\.|dr\s|drg\s)?\s*([\w'\-]+)(.*)$", str(nama_asli).strip(), re.IGNORECASE)
            if match:
                gelar_depan = match.group(1) or "dr. "
                sisa = match.group(3) or ""
                gelar_belakang = ""
                match_belakang = re.search(r"(Sp\.[\w\-]+|Sp\s*[A-Z]+|M\.\w+|drg\.|drh\.|dr\.|dr\s|drg\s)", sisa)
                if match_belakang:
                    gelar_belakang = match_belakang.group(1)
                alias_nama = nama_alias[i % len(nama_alias)]
                alias_map[nama_asli] = f"{gelar_depan.strip()} {alias_nama} {gelar_belakang.strip()}".replace("  ", " ").strip()
            else:
                alias_map[nama_asli] = f"dr. {nama_alias[i % len(nama_alias)]}"
        df['Dokter'] = df['Dokter'].map(alias_map)
    return df

def render_bar_chart(df=None):
    """
    Komponen visualisasi bar chart interaktif di dashboard.
    Menampilkan bar chart kunjungan per dokter spesialis dengan filter.
    """
    st.subheader("Visualisasi: Bar Chart Kunjungan per Dokter Spesialis  (Januari 2024)")
    st.markdown("""
    <div style='background:#f1f8e9;padding:0.7rem 1rem 0.7rem 1rem;border-radius:8px;margin-bottom:1rem;border:1px solid #c5e1a5;'>
        Bar chart ini menampilkan jumlah kunjungan pasien ke masing-masing dokter spesialis di RS Juliana. Gunakan filter di bawah untuk memilih poliklinik dan rentang usia pasien.
    </div>
    """, unsafe_allow_html=True)
    if df is None:
        df = get_barchart_data()
    if df is None or df.empty:
        st.warning("Data tidak tersedia atau kolom penting tidak ditemukan.")
        return
    # Filter interaktif
    poli_list = sorted(df['Poli'].dropna().unique())
    selected_poli = st.multiselect("Filter Poli (opsional):", poli_list, default=poli_list, key="barchart_poli")
    usia_min = int(df['Umur / Tahun'].min())
    usia_max = int(df['Umur / Tahun'].max())
    usia_range = st.slider("Filter Usia (opsional):", usia_min, usia_max, (usia_min, usia_max), key="barchart_usia")
    # Chart di bawah filter
    plot_kunjungan_per_dokter(df, filter_poli=selected_poli, filter_usia=usia_range)

    # Setelah chart/bar chart tampil, tambahkan penjelasan detail di bawah
    st.markdown("""
    <div style='background:#f1f8e9;padding:0.7rem 1rem 0.7rem 1rem;border-radius:8px;margin-top:1.2rem;margin-bottom:0.5rem;border:1px solid #c5e1a5;'>
        <b>Penjelasan:</b><br>
        Grafik ini membantu manajemen memantau distribusi beban kerja dokter dan tren kunjungan pasien per poli. Setiap bar mewakili total kunjungan ke satu dokter spesialis dalam periode data. Anda dapat melakukan analisis lebih spesifik dengan memanfaatkan filter poli dan usia di atas grafik.
    </div>
    """, unsafe_allow_html=True)

# Fungsi utama untuk visualisasi bar chart kunjungan per dokter spesialis
def plot_kunjungan_per_dokter(df, filter_poli=None, filter_usia=None, st_container=None):
    """
    Menampilkan bar chart jumlah kunjungan per dokter spesialis.
    df: DataFrame hasil pembersihan (kolom: 'Poli', 'Dokter', 'Umur / Tahun')
    filter_poli: list poli yang ingin difilter (opsional)
    filter_usia: tuple (min_usia, max_usia) (opsional)
    st_container: Streamlit container (opsional)
    """
    # Filter berdasarkan poli jika diberikan
    if filter_poli is not None and len(filter_poli) > 0:
        df = df[df['Poli'].isin(filter_poli)]
    # Filter berdasarkan usia jika diberikan
    if filter_usia is not None:
        min_usia, max_usia = filter_usia
        df = df[(df['Umur / Tahun'] >= min_usia) & (df['Umur / Tahun'] <= max_usia)]
    # Grouping dan agregasi jumlah kunjungan per dokter
    data_grouped = df.groupby('Dokter').size().reset_index(name='jumlah_kunjungan')
    data_grouped = data_grouped.sort_values('jumlah_kunjungan', ascending=False)
    # Visualisasi bar chart dengan seaborn
    plt.figure(figsize=(10, 6))
    barplot = sns.barplot(
        data=data_grouped,
        x='jumlah_kunjungan',
        y='Dokter',
        hue='Dokter',  # gunakan hue sesuai saran warning
        palette='Greens_d',
        legend=False   # legend tidak perlu karena y unik
    )
    # Tambahkan label jumlah di ujung bar
    for i, v in enumerate(data_grouped['jumlah_kunjungan']):
        barplot.text(v + 0.5, i, str(v), color='black', va='center')
    plt.xlabel('Jumlah Kunjungan')
    plt.ylabel('Dokter Spesialis')
    plt.title('Jumlah Kunjungan per Dokter Spesialis (Januari 2025)')
    plt.tight_layout()
    # Tampilkan plot di Streamlit
    if st_container is not None:
        with st_container:
            st.pyplot(plt)
    else:
        st.pyplot(plt)
    plt.close()

# Contoh penggunaan (untuk pengujian manual, hapus/comment di produksi)
# if __name__ == "__main__":
#     df = pd.read_excel("../../data/original/data_kunjungan_januari.xlsx")
#     plot_kunjungan_per_dokter(df)
