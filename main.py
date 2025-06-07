import streamlit as st
from src.layouting.header import render_header
from src.layouting.footer import render_footer
from src.layouting.sidebar import render_sidebar
from src.visualisasi.daftar_tabel import render_tabel_kunjungan
from src.visualisasi.bar_chart import render_bar_chart
from src.visualisasi_menu import render_visualisasi_menu
from src.tentang import render_tentang

st.set_page_config(
    page_title="Dashboard Kunjungan Rawat Jalan RS Juliana",
    layout="wide"
)

# Embed Bootstrap CSS offline (pastikan sebelum komponen layout dipanggil)
with open("assets/css/bootstrap.min.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

render_header()
render_sidebar()

# Daftar menu dan mapping label ke fungsi
MENU = [
    ("Dashboard Utama", "Dashboard Utama"),
    ("Tabel Data Kunjungan", "Tabel Data Kunjungan"),
    ("Pembersihan Data", "Pembersihan Data"),
    ("Visualisasi", "Visualisasi"),
    ("Tentang", "Tentang")
]

# Sidebar tombol navigasi
if 'selected_menu' not in st.session_state:
    st.session_state['selected_menu'] = MENU[0][0]
selected_menu = st.session_state['selected_menu']

for label, key in MENU:
    if st.sidebar.button(label, key=key, use_container_width=True):
        st.session_state['selected_menu'] = label
        selected_menu = label

if selected_menu == "Dashboard Utama":
    st.title("Dashboard Kunjungan Rawat Jalan RS Juliana - Januari 2024")
    st.write("Selamat datang di dashboard. Silakan pilih menu di sidebar untuk fitur lain.")
elif selected_menu == "Tabel Data Kunjungan":
    render_tabel_kunjungan()
elif selected_menu == "Pembersihan Data":
    st.info("Fitur pembersihan data akan dikembangkan.")
elif selected_menu == "Visualisasi":
    render_visualisasi_menu()
elif selected_menu == "Tentang":
    render_tentang()
else:
    st.write("Aplikasi dashboard visualisasi data RS Juliana. Dibangun dengan Streamlit.")

render_footer()
