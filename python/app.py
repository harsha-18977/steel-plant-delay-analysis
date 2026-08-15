import streamlit as st
st.set_page_config(
    page_title="Steel Plant Delay Analysis",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="collapsed"
)
hide_style = """
<style>
#MainMenu {
    visibility: hidden;}
footer {
    visibility: hidden;
}
header {
    visibility: hidden;
}
section[data-testid="stSidebar"]{
    display:none;
}
.block-container{
    padding-top:2rem;
    padding-bottom:2rem;
}
</style>
"""
st.markdown(hide_style, unsafe_allow_html=True)
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if st.session_state.logged_in:
    st.switch_page("pages/dashboard.py")
else:
    st.switch_page("pages/login.py")