import streamlit as st
from api.service import Auth


def login(username, password):
    auth_service = Auth()
    token_response = auth_service.get_token(username, password)

    if 'error' in token_response:
        st.error(token_response['error'])
        return None
    else:
        st.session_state.token = token_response.get('access', None)
        st.success("Login successful!")
        st.rerun()


def logout():
    for key in st.session_state.keys():
        del st.session_state[key]
    st.success("Logout successful!")
    st.rerun()
