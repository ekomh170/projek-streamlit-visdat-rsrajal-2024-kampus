import streamlit as st

def render_tentang():
    """
    Halaman Tentang Kami yang berfokus pada penjelasan tugas kampus sesuai proposal, dengan tampilan rapi dan sejajar.
    """
    st.title("Tentang Kami")
    st.markdown("""
    <div style="background:#DFF0D8;padding:1.5rem 1.5rem 1rem 1.5rem;border-radius:14px; margin:auto;box-shadow:0 2px 12px rgba(34,139,34,0.10);border:1px solid #e0e0e0;">
      <h2 style="color:#228B22;font-family:Roboto,sans-serif;font-weight:700;margin-bottom:0.7rem;">Penjelasan Tugas Kampus</h2>
      <p style="font-size:1.08rem;color:#444;font-family:Roboto,sans-serif;margin-bottom:1.2rem;">
        Dashboard visualisasi data kunjungan rawat jalan RS Juliana ini merupakan bagian dari tugas proyek mata kuliah <b>Visualisasi Data</b> di STT Terpadu Nurul Fikri.<br><br>
        <b>Deskripsi Tugas:</b><br>
        Mahasiswa diminta membangun dashboard visualisasi data kunjungan rawat jalan dokter spesialis di RS Juliana untuk bulan Januari 2025. Proyek ini bertujuan melatih kemampuan analisis data, pembersihan data, serta pembuatan visualisasi interaktif berbasis web yang bermanfaat untuk manajemen rumah sakit.<br><br>
        <b>Tim Pengembang:</b>
        <ul style="margin-top:0.2rem;margin-bottom:0.7rem;">
          <li>Eko Muchamad Haryono (0110223079) – Ketua Tim</li>
          <li>Raka Muhammad Rabbani (0110223050)</li>
        </ul>
        <b>Dosen Pengampu:</b>
        <ul style="margin-top:0.2rem;margin-bottom:0.7rem;">
          <li>Prodi Teknik Informatika, Kelas SE01, Semester 4, Angkatan 2023</li>
          <li>Mata Kuliah: Visualisasi Data</li>
        </ul>
        <b>Tujuan Tugas:</b>
        <ul style="margin-top:0.2rem;">
          <li>Melatih mahasiswa dalam pengolahan, pembersihan, dan visualisasi data nyata.</li>
          <li>Menghasilkan dashboard yang dapat digunakan untuk pengambilan keputusan di lingkungan rumah sakit.</li>
          <li>Memberikan pengalaman praktik pengembangan aplikasi web data-driven.</li>
        </ul>
      </p>
    </div>
    """, unsafe_allow_html=True)
