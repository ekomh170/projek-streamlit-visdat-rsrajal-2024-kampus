# Dashboard Visualisasi Data Kunjungan Rawat Jalan RS Juliana

## Deskripsi Singkat
Dashboard ini menampilkan visualisasi interaktif data kunjungan rawat jalan dokter spesialis di RS Juliana untuk bulan Januari 2025. Data terhubung otomatis ke Google Spreadsheet, diproses dan divisualisasikan secara periodik (bukan real-time) untuk mendukung pengambilan keputusan manajemen rumah sakit dan pembelajaran mahasiswa.

**Dikembangkan oleh:**
- Eko Muchamad Haryono (0110223079) – Ketua Tim
- Raka Muhammad Rabbani (0110223050)

## Deskripsi Proyek
Aplikasi ini adalah dashboard interaktif untuk memvisualisasikan data kunjungan rawat jalan di RS Juliana bulan Januari 2025. Data diambil otomatis dari Google Spreadsheet, dibersihkan, dan divisualisasikan secara periodik. Dashboard ini membantu manajemen rumah sakit dalam pengambilan keputusan dan juga sebagai media pembelajaran mahasiswa.

## Fitur Utama
- **Integrasi Google Spreadsheet**: Data selalu update otomatis dari link share.
- **Pembersihan Data Otomatis**: Duplikat dihapus, data kosong diisi, format distandarisasi.
- **Visualisasi Interaktif**:
  - Bar Chart: Kunjungan per dokter spesialis
  - Pie Chart: Proporsi pasien berdasarkan jenis kelamin/penjamin
  - Line Graph: Tren kunjungan harian
  - Heatmap: Distribusi berdasarkan hari dan poli
  - Scatter Plot: Usia pasien vs poli
- **Filter Interaktif**: Berdasarkan poli, dokter, usia.
- **Dashboard Web**: Dibangun dengan Streamlit, tema hijau, sidebar filter, notifikasi error jika terjadi kegagalan.

## Tujuan Proyek
Dashboard ini mendukung pengambilan keputusan rumah sakit dan pembelajaran mahasiswa, serta menjadi pondasi awal sistem analisis data rumah sakit yang lebih komprehensif.
