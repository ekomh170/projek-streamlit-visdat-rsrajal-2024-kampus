import streamlit as st
from src.visualisasi.bar_chart import render_bar_chart
from src.visualisasi.pie_chart import render_pie_chart
from src.visualisasi.line_graph import render_line_graph
from src.visualisasi.heatmap import render_heatmap
from src.visualisasi.scatter_plot import render_scatter_plot

# sesuaikan: menu visualisasi utama, Material Design, horizontal radio, dan render visualisasi
def render_visualisasi_menu():
    """
    Halaman utama menu visualisasi, menampilkan pilihan visualisasi dengan tampilan Material Design (ala Google).
    # sesuaikan: menu visualisasi interaktif, horizontal radio, dan pemanggilan fungsi visualisasi
    """
    # Judul halaman
    st.title("Visualisasi Data Kunjungan RS Juliana")
    # Desain Material Design untuk menu visualisasi
    st.markdown("""
    <style>
    .vis-menu-box {
        background: #fff;
        border-radius: 16px;
        padding: 1.5rem 1.5rem 1rem 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 2px 12px rgba(34,139,34,0.10);
        border: 1px solid #e0e0e0;
        max-width: 900px;
        margin-left: auto;
        margin-right: auto;
    }
    .vis-menu-title {
        color: #228B22;
        font-size: 1.4rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        font-family: 'Roboto', Arial, sans-serif;
        letter-spacing: 0.5px;
    }
    .vis-menu-desc {
        color: #444;
        font-size: 1.08rem;
        margin-bottom: 1.2rem;
        font-family: 'Roboto', Arial, sans-serif;
    }
    .vis-radio label {
        font-family: 'Roboto', Arial, sans-serif;
        font-size: 1.08rem;
        color: #228B22;
        font-weight: 500;
        border-radius: 24px;
        padding: 0.4rem 1.2rem;
        margin-right: 0.5rem;
        background: #DFF0D8;
        box-shadow: 0 1px 4px rgba(34,139,34,0.07);
        transition: background 0.2s;
    }
    .vis-radio label[data-selected="true"] {
        background: #228B22;
        color: #fff;
        font-weight: 700;
    }
    </style>
    <div class="vis-menu-box">
        <div class="vis-menu-title">Pilih Jenis Visualisasi</div>
        <div class="vis-menu-desc">Eksplorasi data kunjungan rawat jalan RS Juliana dengan berbagai tipe visualisasi interaktif. Pilih salah satu menu di bawah ini:</div>
    </div>
    """, unsafe_allow_html=True)
    menu = st.radio(
        label="Pilih tipe visualisasi:",
        options=[
            "Bar Chart Kunjungan per Dokter Spesialis",
            "Pie Chart Proporsi Pasien",
            "Line Graph Tren Kunjungan Harian",
            "Heatmap Distribusi Hari & Poli",
            "Scatter Plot Usia vs Poli",
        ],
        key="visualisasi_radio",
        horizontal=True,
        label_visibility="collapsed"
    )
    
    # Tambahkan garis pemisah
    st.markdown("---")
    # Panggil fungsi render sesuai pilihan menu
    if menu == "Bar Chart Kunjungan per Dokter Spesialis":
        render_bar_chart()
    elif menu == "Pie Chart Proporsi Pasien":
        render_pie_chart()
    elif menu == "Line Graph Tren Kunjungan Harian":
        render_line_graph()
    elif menu == "Heatmap Distribusi Hari & Poli":
        render_heatmap()
    elif menu == "Scatter Plot Usia vs Poli":
        render_scatter_plot()
