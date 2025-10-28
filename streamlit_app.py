import streamlit as st
import pandas as pd
from datetime import datetime

# ---------------------------
# PAGE CONFIG
# ---------------------------
st.set_page_config(page_title="Audit Pack Collector", layout="wide")

# ---------------------------
# SESSION STATE
# ---------------------------
if "page" not in st.session_state:
    st.session_state["page"] = "Home"

def go_to(page):
    st.session_state["page"] = page


# ---------------------------
# GLOBAL STYLE
# ---------------------------
st.markdown("""
<style>

/* Remove Streamlit's default top padding */
.block-container {
    padding-top: 0 !important;
}

/* Page background */
[data-testid="stAppViewContainer"] {
    background: #F5F5F5;
    background-attachment: fixed;
}

/* Navbar styling */
.navbar {
    background-color: #000080;
    padding: 1rem 1.5rem;
    box-shadow: 0 2px 6px rgba(0,0,0,0.1);
    position: sticky;
    top: 0;
    z-index: 999;
    text-align: center;
}

/* Navbar title */
.nav-title {
    color: white;
    font-weight: 700;
    font-size: 1.4rem;
    letter-spacing: 0.5px;
    margin-bottom: 0.4rem;
}

/* Navbar buttons container */
.nav-buttons {
    display: flex;
    justify-content: center;
    gap: 1rem;
    margin-top: 0.6rem;
}

/* Default buttons */
.stButton>button {
    background-color: transparent !important;
    color: #FFFFFF !important;
    border: 1px solid transparent !important;
    font-weight: 500;
    border-radius: 6px;
    padding: 0.4rem 1rem;
    transition: all 0.25s ease;
}

/* Hover animation */
.stButton>button:hover {
    transform: scale(1.07);
    background-color: rgba(255,255,255,0.12) !important;
    border-color: rgba(255,255,255,0.3) !important;
}

/* Active page highlight */
button[data-active="true"] {
    background-color: #4CAF50 !important;
    color: white !important;
}

/* Divider line below navbar */
.nav-divider {
    height: 3px;
    background: linear-gradient(90deg, #4CAF50 0%, #FFBF00 100%);
    margin: 0;
    border: none;
}

/* Main content wrapper */
.main-wrapper {
    margin: 2rem auto;
    padding: 2rem 3rem;
    width: 88%;
    background-color: #FFFFFF;
    border-radius: 14px;
    box-shadow: 0 3px 10px rgba(0,0,0,0.05);
}

/* Headings */
h2, h3 {
    color: #000080 !important;
}

/* Metrics styling */
[data-testid="stMetricValue"] {
    color: #000080;
}

</style>
""", unsafe_allow_html=True)


# ---------------------------
# NAVIGATION BAR
# ---------------------------
def navigation_bar():
    st.markdown("""
    <div class="navbar">
        <div class="nav-title">📂 Audit Pack Collector</div>
        <div class="nav-buttons">
    """, unsafe_allow_html=True)

    pages = ["Home", "Upload", "Dashboard", "Login", "SignUp"]
    cols = st.columns(len(pages))
    for i, page in enumerate(pages):
        with cols[i]:
            if st.button(page, key=f"nav_{page}", use_container_width=True):
                go_to(page)

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

with st.container():
    st.markdown('<div class="main-wrapper">', unsafe_allow_html=True)

    # HOME PAGE
    if st.session_state["page"] == "Home":
        st.markdown("## 👋 Welcome to Audit Pack Collector")
        st.write("""
        This platform helps HR and Compliance teams compile, track, and review all documents required for internal or external audits.

        **Key Components**
        - **Central Repository**: All documents in one secure location  
        - **Master Checklist**: Track required vs. collected files  
        - **Responsibility Matrix**: Know who owns what  
        - **Version Control**: Keep only approved versions
        """)
        st.image("https://cdn-icons-png.flaticon.com/512/2991/2991106.png", width=200)
        st.info("Navigate using the menu above to start collecting audit evidence.")

    # UPLOAD PAGE
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

    # DASHBOARD PAGE
    elif st.session_state["page"] == "Dashboard":
        st.header("📊 Audit Dashboard Overview")
        df = st.session_state.audit_items
        completed = df["Status"].eq("Completed").sum()
        total = len(df)
        progress = (completed / total) * 100 if total > 0 else 0

        col1, col2, col3 = st.columns(3)
        col1.metric("Departments", df["Department"].nunique())
        col2.metric("Total Items", total)
        col3.metric("Completed", completed)

        st.progress(progress / 100)
        st.caption(f"✅ {progress:.0f}% of audit items completed")
        st.dataframe(df, use_container_width=True)
        st.caption("💡 Dashboard updates automatically when uploads are completed.")

    # LOGIN PAGE
    elif st.session_state["page"] == "Login":
        st.header("🔐 Login")
        with st.form("login_form"):
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Login")
            if submitted:
                st.success("✅ Logged in (demo only — backend not connected).")

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
                    st.error("❌ Passwords do not match.")
                else:
                    st.success("✅ Account created (demo only — backend not connected).")

    st.markdown("</div>", unsafe_allow_html=True)
