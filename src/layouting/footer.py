"""
Komponen footer untuk dashboard Streamlit RS Juliana
"""
import streamlit as st

def render_footer():
    st.markdown("""
        <hr style='margin-top:32px;margin-bottom:8px;'>
        <div style='text-align:center;font-size:0.95rem;color:#888;'>
            &copy; 2025 RS Juliana | Dibangun dengan Streamlit<br>
            <span style='font-size:0.93rem;color:#888;'>Developer: Eko Muchamad Haryono - 0110223079 (Ketua Tim) &amp; Raka Muhammad Rabbani - 0110223050</span>
        </div>
    """, unsafe_allow_html=True)
