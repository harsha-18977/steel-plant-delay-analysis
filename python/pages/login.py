import streamlit as st
import mysql.connector

# -------------------------------------
# PAGE CONFIG
# -------------------------------------

st.set_page_config(
    page_title="Steel Plant Login",
    page_icon="🏭",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# -------------------------------------
# CUSTOM CSS
# -------------------------------------

st.markdown("""
<style>

#MainMenu{
    visibility:hidden;
}

footer{
    visibility:hidden;
}

header{
    visibility:hidden;
}

section[data-testid="stSidebar"]{
    display:none;
}

.stApp{
    background:lightblue;
}

.login-card{

    background:white;

    padding:35px;

    border-radius:20px;

    box-shadow:0px 5px 20px rgba(0,0,0,0.15);

}

</style>
""", unsafe_allow_html=True)

# -------------------------------------
# CENTER LOGO
# -------------------------------------

col1, col2, col3 = st.columns([1,2,1])

with col2:

    st.image(
    "assets/Rashtriya_Ispat_Nigam.svg",
    width=140
)
    

# -------------------------------------
# TITLE
# -------------------------------------

st.markdown(
"""
<h1 style='text-align:center;
color:#003B73;
font-size:52px;
font-weight:bold;'>

Steel Plant Delay Analysis

</h1>
""",
unsafe_allow_html=True
)

st.markdown(
"""
<div style='text-align:center;
font-size:24px;
color:lightblack;
margin-bottom:40px;'>

Rashtriya Ispat Nigam Limited (Vizag Steel)

</div>
""",
unsafe_allow_html=True
)

st.write("")

# -------------------------------------
# LOGIN FORM
# -------------------------------------

username = st.text_input(
    "👤 Username"
)

password = st.text_input(
    "🔒 Password",
    type="password"
)

st.write("")

if st.button("LOGIN"):

    connection = mysql.connector.connect(

        host="localhost",

        user="root",

        password="vardhansql@004",

        database="steel_delay_analysis"

    )

    cursor = connection.cursor()

    query = """
    SELECT *
    FROM users
    WHERE username=%s
    AND password=%s
    """

    cursor.execute(

        query,

        (username, password)

    )

    user = cursor.fetchone()

    if user:

        st.session_state.logged_in = True

        st.session_state.username = username

        st.success("✅ Login Successful")

        st.switch_page("pages/dashboard.py")

    else:

        st.error("❌ Invalid Username or Password")

    connection.close()

st.write("")
st.write("")

st.markdown(
"""
<div style='text-align:center;color:gray;'>

Internship Project 2026

Steel Plant Delay Analysis & Prediction System

</div>
""",
unsafe_allow_html=True
)