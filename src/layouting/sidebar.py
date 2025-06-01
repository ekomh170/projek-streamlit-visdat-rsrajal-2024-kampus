"""
Komponen sidebar untuk dashboard Streamlit RS Juliana
Mengadopsi prinsip Material Design/Bootstrap, offline-ready (CSS lokal).
"""
import streamlit as st

def render_sidebar():
    st.sidebar.markdown(
        '''
        <div class="d-flex flex-column align-items-center p-3">
            <img src="https://i.ibb.co/6b7n6Qw/hospital-logo.png" class="rounded shadow mb-3" width="90">
            <h2 class="text-success fw-bold mb-2" style="font-family:Roboto,sans-serif;">Menu Navigasi</h2>
        </div>
        <div class="mt-3 text-secondary text-center" style="font-size:0.95rem;">
            <span style="font-family:Roboto,sans-serif;">Gunakan menu di bawah untuk navigasi.</span>
        </div>
        ''',
        unsafe_allow_html=True
    )
