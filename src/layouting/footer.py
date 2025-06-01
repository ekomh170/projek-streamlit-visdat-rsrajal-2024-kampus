"""
Komponen footer untuk dashboard Streamlit RS Juliana
"""
import streamlit as st

def render_footer():
    st.markdown("""
        <hr style='margin-top:32px;margin-bottom:8px;'>
        <div style='text-align:center;font-size:0.95rem;color:#888;'>
            &copy; 2025 RS Juliana | Dibangun dengan Streamlit 389
        </div>
    """, unsafe_allow_html=True)
