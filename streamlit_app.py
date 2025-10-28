import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Audit Pack Collector", layout="wide")

# ---------------------------
# SESSION STATE
# ---------------------------
if "page" not in st.session_state:
    st.session_state["page"] = "Home"

def go_to(page):
    st.session_state["page"] = page

# ---------------------------
# CUSTOM CSS
# ---------------------------
st.markdown("""
<style>
/* Remove Streamlit's top padding */
.block-container {
    padding-top: 0 !important;
}

/* Background gradient */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(160deg, #f8faff 0%, #eef3ff 50%, #f4f7ff 100%);
    background-attachment: fixed;
}

/* Navbar */
.navbar {
    background-color: #ffffff;
    padding: 0.8rem 1.2rem;
    box-shadow: 0 2px 6px rgba(0,0,0,0.08);
    position: sticky;
    top: 0;
    z-index: 1000;
    text-align: center;
}

/* Title inside navbar */
.nav-title {
    color: #0d6efd;
    font-weight: 700;
    font-size: 1.4rem;
    margin-bottom: 0.4rem;
}

/* Blue divider line */
.nav-divider {
    height: 3px;
    background: linear-gradient(90deg, #0d6efd 0%, #7ba7ff 100%);
    margin: 0;
    border: none;
}

/* Center navbar buttons */
.nav-buttons {
    display: flex;
    justify-content: center;
    gap: 1rem;
    margin-top: 0.6rem;
}

/* Buttons styling */
.stButton>button {
    background-color: transparent !important;
    color: #0d6efd !important;
    border: none !important;
    font-weight: 500;
    font-size: 0.95rem;
    border-radius: 6px;
    padding: 0.4rem 1rem;
    transition: all 0.2s ease-in-out;
}

/* Hover animation */
.stButton>button:hover {
    transform: scale(1.05);
    background-color: rgba(13, 110, 253, 0.06) !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.08);
}

/* Main container (remove top margin to kill white bar) */
.main-container {
    background-color: white;
    padding: 2rem 3rem;
    border-radius: 18px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    margin: 0 auto 2rem auto;
    width: 85%;
}
</style>
""", unsafe_allow_html=True)


# ---------------------------
# NAVIGATION BAR
# ---------------------------
def navigation_bar():
    st.markdown("""
    <div class="navbar">
        <div class="nav-title">📦 Audit Pack Collector</div>
        <div class="nav-buttons">
    """, unsafe_allow_html=True)

    cols = st.columns(5)
    with cols[0]:
        if st.button("🏠 Home"): go_to("Home")
    with cols[1]:
        if st.button("📁 Upload"): go_to("Upload")
    with cols[2]:
        if st.button("📊 Dashboard"): go_to("Dashboard")
    with cols[3]:
        if st.button("🔐 Login"): go_to("Login")
    with cols[4]:
        if st.button("🧾 Sign Up"): go_to("SignUp")

    st.markdown("""
        </div>
    </div>
    <div class="nav-divider"></div>
    """, unsafe_allow_html=True)


# ---------------------------
# DUMMY DATA
# ---------------------------
if "audit_items" not in st.session_state:
    st.session_state.audit_items = pd.DataFrame({
        "Department": ["HR", "Finance", "IT", "Operations"],
        "Document": ["Training Records", "Payroll Compliance", "System Access Logs", "Safety Certificates"],
        "Status": ["Pending", "Pending", "Pending", "Pending"],
        "Last Updated": ["", "", "", ""],
    })


# ---------------------------
# PAGE CONTENTS
# ---------------------------
navigation_bar()
st.markdown('<div class="main-container">', unsafe_allow_html=True)

if st.session_state["page"] == "Home":
    st.markdown("## 👋 Welcome to Audit Pack Collector")
    st.write("""
        A modern tool for HR and Compliance teams to collect and track all audit documents efficiently.

        **Core Features**
        - 📋 Centralized audit checklist  
        - 📁 File upload & evidence tracking  
        - 📊 Progress visualization  
        - 🔐 Login and sign-up (demo only)
    """)
    st.image("https://cdn-icons-png.flaticon.com/512/2991/2991106.png", width=200)
    st.info("Use the navigation bar above to switch pages.")


elif st.session_state["page"] == "Upload":
    st.header("📁 Upload Audit Evidence")
    dept = st.selectbox("Select Department", st.session_state.audit_items["Department"])
    doc_type = st.selectbox(
        "Select Document Type",
        st.session_state.audit_items.query("Department == @dept")["Document"]
    )
    uploaded_file = st.file_uploader("Upload File", type=["pdf", "docx", "jpg", "png"])
    if uploaded_file:
        st.success(f"✅ File '{uploaded_file.name}' uploaded for {dept} - {doc_type}")
        idx = st.session_state.audit_items.query("Department == @dept and Document == @doc_type").index[0]
        st.session_state.audit_items.loc[idx, "Status"] = "Completed"
        st.session_state.audit_items.loc[idx, "Last Updated"] = datetime.now().strftime("%Y-%m-%d %H:%M")


elif st.session_state["page"] == "Dashboard":
    st.header("📊 Audit Dashboard")
    df = st.session_state.audit_items
    completed = df["Status"].eq("Completed").sum()
    total = len(df)
    progress = (completed / total) * 100

    col1, col2, col3 = st.columns(3)
    col1.metric("Departments", df["Department"].nunique())
    col2.metric("Total Items", total)
    col3.metric("Completed", completed)

    st.progress(progress / 100)
    st.caption(f"✅ {progress:.0f}% of audit items completed")

    st.dataframe(df, use_container_width=True)
    st.caption("💡 Dashboard updates automatically when uploads are completed.")


elif st.session_state["page"] == "Login":
    st.header("🔐 Login")
    with st.form("login_form"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")
        if submitted:
            st.success("✅ Logged in (demo only — backend not connected).")


elif st.session_state["page"] == "SignUp":
    st.header("🧾 Create an Account")
    with st.form("signup_form"):
        name = st.text_input("Full Name")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        confirm = st.text_input("Confirm Password", type="password")
        submitted = st.form_submit_button("Sign Up")
        if submitted:
            if password != confirm:
                st.error("Passwords do not match.")
            else:
                st.success("✅ Account created (demo only — backend not connected).")

st.markdown("</div>", unsafe_allow_html=True)
