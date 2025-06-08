import streamlit as st
import os  # sesuaikan: untuk path absolut favicon
from src.layouting.header import render_header
from src.layouting.footer import render_footer
from src.layouting.sidebar import render_sidebar
from src.visualisasi.daftar_tabel import render_tabel_kunjungan
from src.visualisasi_menu import render_visualisasi_menu
from src.tentang import render_tentang
from src.pembersihan_data import render_pembersihan_data 
from src.dashboard_intro import render_dashboard_intro

st.set_page_config(
    page_title="Dashboard Kunjungan Rawat Jalan RS Juliana",
    layout="wide",
    # sesuaikan: favicon pakai path absolut jika ada, fallback emoji jika tidak
    page_icon=os.path.abspath("assets/img/favicon/favicon.ico") if os.path.exists("assets/img/favicon/favicon.ico") else "🏥"
)

# Embed Bootstrap CSS offline (pastikan sebelum komponen layout dipanggil)
with open("assets/css/bootstrap.min.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Render header dan sidebar
render_header()
render_sidebar()

# Daftar menu dan mapping label ke fungsi
MENU = [
    ("Dashboard Utama", "Dashboard Utama"),
    ("Tabel Data Kunjungan", "Tabel Data Kunjungan"),
    ("Visualisasi Data", "Visualisasi Data"),
    ("Pembersihan Data", "Pembersihan Data"),
    ("Tentang", "Tentang")
]

# Sidebar tombol navigasi
# Pastikan session state untuk menu sudah ada
if 'selected_menu' not in st.session_state:
    st.session_state['selected_menu'] = MENU[0][0]
selected_menu = st.session_state['selected_menu']

# Render tombol menu di sidebar
for label, key in MENU:
    if st.sidebar.button(label, key=key, use_container_width=True):
        st.session_state['selected_menu'] = label
        selected_menu = label

# Render konten berdasarkan menu yang dipilih
if selected_menu == "Dashboard Utama":
    render_dashboard_intro()
elif selected_menu == "Tabel Data Kunjungan":
    render_tabel_kunjungan()
elif selected_menu == "Visualisasi Data":
    render_visualisasi_menu()
elif selected_menu == "Pembersihan Data":
    render_pembersihan_data()
elif selected_menu == "Tentang":
    render_tentang()
else:
    st.write("Aplikasi dashboard visualisasi data RS Juliana. Dibangun dengan Streamlit.")

render_footer()
