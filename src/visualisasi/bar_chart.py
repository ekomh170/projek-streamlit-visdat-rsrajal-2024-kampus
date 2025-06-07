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
    return df

def render_bar_chart(df=None):
    """
    Komponen visualisasi bar chart interaktif di dashboard.
    Menampilkan bar chart kunjungan per dokter spesialis dengan filter.
    """
    st.subheader("Visualisasi: Bar Chart Kunjungan per Dokter Spesialis")
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
