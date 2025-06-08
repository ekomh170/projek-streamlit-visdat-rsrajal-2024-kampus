import streamlit as st

def render_tentang():
    """
    Halaman Tentang Kami untuk dashboard visualisasi RS Juliana.
    """
    st.title("Tentang Kami")
    st.markdown("""
    <div style="background:#DFF0D8;padding:1.5rem 1.5rem 1rem 1.5rem;border-radius:14px;max-width:900px;margin:auto;box-shadow:0 2px 12px rgba(34,139,34,0.10);border:1px solid #e0e0e0;">
    <h2 style="color:#228B22;font-family:Roboto,sans-serif;font-weight:700;">Dashboard Visualisasi Data Kunjungan Rawat Jalan RS Juliana</h2>
    <p style="font-size:1.08rem;color:#444;font-family:Roboto,sans-serif;">
    Dashboard ini dikembangkan sebagai solusi cerdas untuk membantu manajemen RS Juliana dalam memantau, menganalisis, dan mengambil keputusan berbasis data kunjungan rawat jalan. Sistem ini terintegrasi langsung dengan Google Spreadsheet, sehingga data selalu update dan kolaboratif.<br><br>
    <b>Fitur utama:</b>
    <ul>
      <li>Visualisasi interaktif (bar chart, pie chart, line graph, heatmap, scatter plot)</li>
    </ul>
    <b>Tim Pengembang:</b><br>
    <ul>
      <li>Eko Muchamad Haryono - 0110223079 - Mahasiswa (Ketua Tim)</li>
      <li>Raka Muhammad Rabbani - 0110223050 - Mahasiswa</li>
    </ul>
    <b>Tujuan:</b><br>
    <ul>
      <li>Mendukung pengambilan keputusan berbasis data di lingkungan rumah sakit</li>
      <li>Media pembelajaran mahasiswa dalam visualisasi data dan pengembangan aplikasi web</li>
      <li>Pondasi awal sistem analitik data rumah sakit yang lebih komprehensif</li>
    </ul>
    <b>Kontak:</b><br>
    <ul>
      <li>Website : <a href="https://rsjuliana.co.id" target="_blank">https://rsjuliana.co.id</a></li>
    </ul>
    </p>
    </div>
    """, unsafe_allow_html=True)
