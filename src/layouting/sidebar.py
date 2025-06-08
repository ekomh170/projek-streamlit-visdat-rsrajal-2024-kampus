"""
Komponen sidebar untuk dashboard Streamlit RS Juliana
Mengadopsi prinsip Material Design/Bootstrap, offline-ready (CSS lokal).
# sesuaikan: logo dan layout sidebar
"""
import streamlit as st

def render_sidebar():
    st.sidebar.image("assets/img/rsjuliana.png", width=110)  # sesuaikan: logo RS Juliana lokal
    st.sidebar.markdown(
        '''
        <div class="d-flex flex-column align-items-center p-3" style="margin-top:-10px; margin-bottom:0;">
            <h2 class="text-success fw-bold mb-2" style="font-family:Roboto,sans-serif; margin-bottom:0.5rem;">Menu Navigasi</h2>
        </div>
        <div class="text-secondary text-center" style="font-size:0.95rem; margin-top:-10px; margin-bottom:0.5rem;">
            <span style="font-family:Roboto,sans-serif;">Gunakan menu di bawah untuk navigasi.</span>
        </div>
        ''',
        unsafe_allow_html=True
    )
