"""
Komponen header untuk dashboard Streamlit RS Juliana
"""
import streamlit as st

def render_header(title: str = "Dashboard Kunjungan Rawat Jalan RS Juliana"):
    st.markdown(f"""
        <div style='background-color:#228B22;padding:16px 0 8px 0;margin-bottom:16px;'>
            <h1 style='color:white;text-align:center;margin:0;font-size:2.2rem;'>{title}</h1>
        </div>
    """, unsafe_allow_html=True)
