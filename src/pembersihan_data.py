import streamlit as st
import os
from src.data_handler.spreadsheet_connector import cek_koneksi_gspread

def render_pembersihan_data():
    """
    Halaman pembersihan data: cek koneksi Google Spreadsheet.
    """
    st.title("Pembersihan Data Kunjungan RS Juliana")
    st.markdown("""
    <div style='background:#DFF0D8;padding:1.1rem 1.5rem 1rem 1.5rem;border-radius:14px;max-width:700px;margin-bottom:1.2rem;box-shadow:0 2px 12px rgba(34,139,34,0.10);border:1px solid #e0e0e0;'>
        Halaman ini memastikan koneksi ke sumber data Google Spreadsheet berjalan dengan baik.
    </div>
    """, unsafe_allow_html=True)
    if st.button("Cek Koneksi Google Spreadsheet"):
        creds_path = os.path.join("json", "credentials.json")
        try:
            status, pesan = cek_koneksi_gspread(creds_path=creds_path)
            if status:
                st.success(pesan)
                st.balloons()
                st.markdown("""
                <div style='background:#e8f5e9;padding:0.8rem 1.2rem 0.8rem 1.2rem;border-radius:10px;margin-top:0.5rem;margin-bottom:1rem;border:1px solid #b2dfdb;'>
                    <b>✔️ Koneksi ke Google Spreadsheet berhasil!</b><br>
                    Service account sudah terautentikasi dan siap mengambil data dari Google Sheets.<br>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.error(pesan)
        except Exception as e:
            st.error(f"Terjadi error saat cek koneksi: {e}")