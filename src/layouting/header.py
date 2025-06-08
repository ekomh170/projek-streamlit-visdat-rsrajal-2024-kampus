"""
Komponen header untuk dashboard Streamlit RS Juliana
"""
import streamlit as st

def render_header(title: str = "Visualisasi Kunjungan Rawat Jalan RS Juliana – Januari 2024"):
    st.markdown(f"""
<div style='background:linear-gradient(90deg,#228B22 60%,#43a047 100%); padding:22px 0 14px 0; margin-bottom:20px; border-radius:0 0 18px 18px; box-shadow:0 2px 12px rgba(34,139,34,0.10); border-bottom:4px solid #c5e1a5;'>
    <h1 style='color:white; text-align:center; margin:0; font-size:2.1rem; font-family:Roboto,sans-serif; font-weight:700; letter-spacing:0.5px; text-shadow:0 2px 8px rgba(0,0,0,0.10);'>
        Visualisasi Kunjungan Rawat Jalan<br>RS Juliana – Januari 2024
    </h1>
</div>
""", unsafe_allow_html=True)
