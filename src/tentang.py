import streamlit as st

def render_tentang():
    """
    Halaman Tentang Kami yang berfokus pada penjelasan tugas kampus, alasan pemilihan tema, identitas mahasiswa, dan dosen pengampu, dengan jarak antar elemen yang lebih padat dan natural.
    """
    st.title("Tentang Kami")
    st.markdown("""
    <div style="background:#DFF0D8;padding:1.5rem 1.5rem 1rem 1.5rem;border-radius:14px;margin:auto;box-shadow:0 2px 12px rgba(34,139,34,0.10);border:1px solid #e0e0e0;">
      <h2 style="color:#228B22;font-family:Roboto,sans-serif;font-weight:700;margin-bottom:1rem;">Penjelasan Tugas Kampus</h2>
      <div style="font-size:1.08rem;color:#222;font-family:Roboto,sans-serif;line-height:1.7;">
        <p style="margin-bottom:1.1rem;">
          Dashboard visualisasi data kunjungan rawat jalan RS Juliana ini merupakan bagian dari tugas proyek mata kuliah <b>Visualisasi Data</b> di STT Terpadu Nurul Fikri.
        </p>
        <b style="font-family:Roboto,sans-serif;">Deskripsi Tugas:</b>
        <p style="margin-bottom:1.1rem;">
          Mahasiswa diminta mengelola dan memvisualisasikan 1.000 data sebagai bagian dari tugas proyek. Kami memilih tema data kunjungan rawat jalan dokter spesialis di RS Juliana untuk bulan Januari 2024 karena salah satu anggota tim, Eko, memiliki rekan kerja di rumah sakit tersebut sehingga memudahkan akses data dan pemahaman konteks nyata. Proyek ini bertujuan untuk melatih kemampuan analisis data, pembersihan data, serta pembuatan visualisasi interaktif berbasis web yang bermanfaat bagi manajemen rumah sakit.
        </p>
        <b style="font-family:Roboto,sans-serif;">Tim Pengembang:</b>
        <ul style="margin-top:0.2rem;margin-bottom:1.1rem;font-family:Roboto,sans-serif;">
          <li>Eko Muchamad Haryono (0110223079) – Ketua Tim</li>
          <li>Raka Muhammad Rabbani (0110223050)</li>
        </ul>
        <b style="font-family:Roboto,sans-serif;">Identitas Mahasiswa:</b>
        <ul style="margin-top:0.2rem;margin-bottom:1.1rem;font-family:Roboto,sans-serif;">
          <li>Prodi: Teknik Informatika</li>
          <li>Kelas: SE01</li>
          <li>Semester: 4</li>
          <li>Angkatan: 2023</li>
        </ul>
        <b style="font-family:Roboto,sans-serif;">Dosen Pengampu:</b>
        <ul style="margin-top:0.2rem;margin-bottom:1.1rem;font-family:Roboto,sans-serif;">
          <li>Imam Haromain, S.Si., M.Kom.</li>
        </ul>
        <b style="font-family:Roboto,sans-serif;">Tujuan Tugas:</b>
        <ul style="margin-top:0.2rem;margin-bottom:0.2rem;font-family:Roboto,sans-serif;">
          <li>Melatih mahasiswa dalam pengolahan, pembersihan, dan visualisasi data nyata.</li>
          <li>Menghasilkan dashboard yang dapat digunakan untuk pengambilan keputusan di lingkungan rumah sakit.</li>
          <li>Memberikan pengalaman praktik pengembangan aplikasi web menggunakan Streamlit.</li>
          <li>Menyelesaikan tugas proyek mata kuliah Visualisasi Data.</li>
        </ul>
      </div>
    </div>
    """, unsafe_allow_html=True)
