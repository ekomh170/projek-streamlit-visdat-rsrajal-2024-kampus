import streamlit as st

def render_dashboard_intro():
    """
    Komponen deskripsi singkat, tujuan dashboard utama, teknologi yang digunakan (termasuk API), dan ringkasan ruang lingkup sesuai proposal.
    """
    st.title("Dashboard Kunjungan Rawat Jalan RS Juliana - Januari 2024")
    st.markdown("""
    <div style='background:#f1f8e9;padding:1.2rem 1.6rem 1.2rem 1.6rem;border-radius:13px;margin-bottom:1.7rem;border:1px solid #c5e1a5;'>
        <b>Deskripsi & Tujuan Dashboard</b><br>
        Dashboard ini dikembangkan sebagai solusi visualisasi data kunjungan rawat jalan dokter spesialis di RS Juliana selama bulan Januari 2024. Dengan memanfaatkan data real dari SIMRS, dashboard ini bertujuan untuk <b>membantu manajemen dan staf rumah sakit dalam memantau, menganalisis, serta mengambil keputusan berbasis data</b> secara cepat dan akurat.<br><br>
        <b>Ruang Lingkup & Permasalahan:</b><br>
        <ul style='margin-bottom:0.2rem;'>
            <li>Fokus pada data kunjungan rawat jalan bulan Januari 2024 (sekitar 6.000 entri).</li>
            <li>Analisis utama pada pelayanan poliklinik dan dokter spesialis, tidak mencakup IGD, rawat inap, atau farmasi.</li>
            <li>Visualisasi distribusi pasien berdasarkan poli, usia, jenis kelamin, penjamin, dan tren harian.</li>
            <li>Identifikasi dokter dengan volume kunjungan tertinggi/terendah, hari tersibuk, dan pola kunjungan.</li>
        </ul>
        <b>Kenapa dashboard ini penting?</b><br>
        <ul style='margin-bottom:0.2rem;'>
            <li>Memudahkan identifikasi tren kunjungan, distribusi pasien, dan kinerja dokter spesialis.</li>
            <li>Menyajikan insight visual yang informatif untuk mendukung perencanaan jadwal, alokasi sumber daya, dan evaluasi layanan.</li>
            <li>Mempercepat proses analisis data tanpa perlu keahlian teknis lanjutan.</li>
            <li>Menjadi media pembelajaran mahasiswa dalam praktik visualisasi data kesehatan.</li>
        </ul>
        <b>Fitur Utama:</b>
        <ul style='margin-bottom:0.2rem;'>
            <li>Visualisasi interaktif: bar chart, pie chart, line graph, heatmap, dan scatter plot.</li>
            <li>Analisis distribusi pasien berdasarkan poli, usia, jenis kelamin, dan penjamin.</li>
            <li>Identifikasi dokter dengan volume kunjungan tertinggi dan terendah.</li>
            <li>Insight hari tersibuk dan pola kunjungan harian.</li>
        </ul>
        <b>Manfaat:</b>
        <ul style='margin-bottom:0.2rem;'>
            <li>Mendukung pengambilan keputusan manajerial berbasis data.</li>
            <li>Optimalisasi jadwal dokter dan kapasitas layanan.</li>
            <li>Privasi data terjaga, data telah dianonimkan sesuai etika kesehatan.</li>
        </ul>
        <b>Teknologi yang Digunakan:</b>
        <ul style='margin-bottom:0.2rem;'>
            <li><b>Python</b> sebagai bahasa pemrograman utama untuk analisis dan visualisasi data.</li>
            <li><b>Streamlit</b> untuk membangun dashboard web interaktif yang mudah digunakan.</li>
            <li><b>Pandas</b> untuk manipulasi dan pembersihan data.</li>
            <li><b>Matplotlib</b> & <b>Seaborn</b> untuk pembuatan grafik dan visualisasi statistik.</li>
            <li><b>Microsoft Excel</b> sebagai format awal data hasil ekspor dari SIMRS.</li>
            <li><b>Google Colab</b> untuk kolaborasi dan eksperimen kode Python secara cloud-based.</li>
            <li><b>Google Sheets API</b> & <b>Google Drive API</b> untuk integrasi dan sinkronisasi data otomatis dari spreadsheet rumah sakit ke dashboard.</li>
            <li><b>Streamlit Cache</b> dan <b>File Pickle</b> untuk menyimpan data hasil olahan sementara, sehingga loading data dan visualisasi lebih cepat serta efisien.</li>
        </ul>
        <b>Target Pengguna:</b>
        <ul style='margin-bottom:0.2rem;'>
            <li>Manajemen RS Juliana, staf medis, bagian rekam medis, administrasi, dan mahasiswa.</li>
        </ul>
        <br>
        <i>Jelajahi menu di sidebar untuk melihat data, visualisasi, dan insight lebih lanjut. Dashboard ini adalah langkah awal menuju sistem analitik rumah sakit yang lebih modern dan efisien.</i>
    </div>
    """, unsafe_allow_html=True)
