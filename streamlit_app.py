import streamlit as st
import pandas as pd
from datetime import datetime

# ---------------------------
# CONFIG
# ---------------------------
st.set_page_config(page_title="Audit Pack Collector", layout="wide")

if "page" not in st.session_state:
    st.session_state["page"] = "Home"

def go_to(page_name):
    st.session_state["page"] = page_name


# ---------------------------
# STYLE (HR PROFESSIONAL THEME)
# ---------------------------
st.markdown("""
<style>
/* Global background */
[data-testid="stAppViewContainer"] {
    background-color: #F5F5F5 !important;
}

/* Remove top default padding */
.block-container {
    padding-top: 0 !important;
}

/* Navbar styling */
.navbar {
    background-color: #000080;
    color: white;
    padding: 1rem 2rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    box-shadow: 0 3px 6px rgba(0,0,0,0.15);
    position: sticky;
    top: 0;
    z-index: 999;
}

.navbar-title {
    font-weight: 700;
    font-size: 1.3rem;
}

.nav-links {
    display: flex;
    gap: 1rem;
}

.nav-button {
    background: transparent;
    color: #FFFFFF;
    border: 2px solid transparent;
    padding: 0.4rem 1rem;
    border-radius: 6px;
    font-weight: 500;
    transition: all 0.25s ease;
    cursor: pointer;
}

.nav-button:hover {
    background-color: rgba(255,255,255,0.1);
    transform: scale(1.05);
}

.nav-active {
    border-bottom: 2px solid #4CAF50;
}

/* Main content container (no extra white box wrapper) */
.main-section {
    margin: 2rem auto;
    padding: 2rem 3rem;
    width: 90%;
    background-color: #FFFFFF;
    border-radius: 12px;
    box-shadow: 0 3px 8px rgba(0,0,0,0.05);
}

/* Buttons */
.stButton > button {
    background-color: #4CAF50 !important;
    color: white !important;
    font-weight: 600;
    border: none;
    border-radius: 6px;
    padding: 0.5rem 1.2rem;
    transition: all 0.2s ease;
}

.stButton > button:hover {
    background-color: #45a049 !important;
    transform: scale(1.05);
}

/* Status colors */
.status-complete {
    color: #4CAF50;
    font-weight: 600;
}

.status-pending {
    color: #FFBF00;
    font-weight: 600;
}
</style>
""", unsafe_allow_html=True)


# ---------------------------
# NAVBAR
# ---------------------------
def navigation_bar():
    st.markdown('<div class="navbar">', unsafe_allow_html=True)
    st.markdown('<div class="navbar-title">📂 Audit Pack Collector</div>', unsafe_allow_html=True)

    pages = ["Home", "Upload", "Dashboard", "Login", "SignUp"]
    st.markdown('<div class="nav-links">', unsafe_allow_html=True)

    nav_cols = st.columns(len(pages))
    for i, page in enumerate(pages):
        is_active = "nav-button nav-active" if st.session_state["page"] == page else "nav-button"
        with nav_cols[i]:
            if st.button(page, key=f"nav_{page}"):
                go_to(page)
    st.markdown('</div></div>', unsafe_allow_html=True)


# ---------------------------
# DUMMY DATA
# ---------------------------
if "audit_items" not in st.session_state:
    st.session_state.audit_items = pd.DataFrame({
        "Department": ["HR", "Finance", "IT", "Operations"],
        "Document": ["Training Records", "Payroll Compliance", "System Access Logs", "Safety Certificates"],
        "Status": ["Pending", "Pending", "Pending", "Pending"],
        "Owner": ["Jane", "John", "Lily", "Adam"],
        "Reviewer": ["Mary", "Tom", "Anna", "Robert"],
        "Last Updated": ["", "", "", ""],
    })


# ---------------------------
# MAIN CONTENT AREA
# ---------------------------
navigation_bar()

with st.container():
    st.markdown('<div class="main-section">', unsafe_allow_html=True)

    # HOME PAGE
    if st.session_state["page"] == "Home":
        st.markdown("## 👋 Welcome to the Audit Pack Collector System")
        st.write("""
        A simple and secure way for HR & Compliance teams to manage their audit documentation process.

        **Core Features**
        - 🧾 Central Repository for all documents  
        - 📋 Master Checklist with Responsibilities  
        - 👤 Ownership & Review Tracking  
        - 📅 Version Control and Audit Progress  
        """)
        st.image("https://cdn-icons-png.flaticon.com/512/2991/2991106.png", width=180)
        st.info("Use the menu above to upload documents or track audit completion.")

    # UPLOAD PAGE
    elif st.session_state["page"] == "Upload":
        st.header("📁 Upload Audit Documents")
        dept = st.selectbox("Select Department", st.session_state.audit_items["Department"])
        doc_type = st.selectbox("Select Document", st.session_state.audit_items.query("Department == @dept")["Document"])
        file = st.file_uploader("Upload File", type=["pdf", "docx", "xlsx", "jpg", "png"])
        if file:
            st.success(f"✅ Uploaded: {file.name} for {dept} - {doc_type}")
            idx = st.session_state.audit_items.query("Department == @dept and Document == @doc_type").index[0]
            st.session_state.audit_items.loc[idx, "Status"] = "Completed"
            st.session_state.audit_items.loc[idx, "Last Updated"] = datetime.now().strftime("%Y-%m-%d %H:%M")

    # DASHBOARD PAGE
    elif st.session_state["page"] == "Dashboard":
        st.header("📊 Audit Progress Dashboard")
        df = st.session_state.audit_items
        total = len(df)
        completed = df["Status"].eq("Completed").sum()
        progress = int((completed / total) * 100)

        col1, col2, col3 = st.columns(3)
        col1.metric("Departments", df["Department"].nunique())
        col2.metric("Documents", total)
        col3.metric("Completion", f"{progress}%")

        st.progress(progress / 100)
        st.dataframe(df.style.applymap(
            lambda v: "color:#4CAF50" if v == "Completed" else "color:#FFBF00",
            subset=["Status"]
        ), use_container_width=True)

    # LOGIN PAGE
    elif st.session_state["page"] == "Login":
        st.header("🔐 Login")
        with st.form("login_form"):
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Login")
            if submitted:
                st.success("✅ Logged in (demo only).")

    # SIGNUP PAGE
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
                    st.success("✅ Account created (demo only).")

    st.markdown('</div>', unsafe_allow_html=True)
