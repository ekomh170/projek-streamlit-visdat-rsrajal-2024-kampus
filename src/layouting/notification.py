"""
Komponen notifikasi/info untuk dashboard Streamlit RS Juliana
"""
import streamlit as st

def show_notification(message: str, type_: str = "info"):
    if type_ == "info":
        st.info(message)
    elif type_ == "success":
        st.success(message)
    elif type_ == "warning":
        st.warning(message)
    elif type_ == "error":
        st.error(message)
    else:
        st.write(message)
