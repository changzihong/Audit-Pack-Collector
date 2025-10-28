import streamlit as st
import pandas as pd
from datetime import datetime

# ---------------------------
# PAGE CONFIG
# ---------------------------
st.set_page_config(page_title="Audit Pack Collector", layout="wide")

# ---------------------------
# SESSION STATE SETUP
# ---------------------------
if "page" not in st.session_state:
    st.session_state["page"] = "Home"

def go_to(page_name):
    st.session_state["page"] = page_name


# ---------------------------
# NAVIGATION BAR (BUTTON STYLE)
# ---------------------------
def navigation_bar():
    st.markdown(
        """
        <style>
            div[data-testid="stHorizontalBlock"] {
                background-color: #0d6efd;
                padding: 0.8rem 1.2rem;
                border-radius: 8px;
                display: flex;
                justify-content: space-between;
                align-items: center;
            }
            .nav-btn {
                background-color: white;
                color: #0d6efd;
                border-radius: 8px;
                padding: 0.4rem 0.9rem;
                border: none;
                font-weight: 500;
                cursor: pointer;
            }
            .nav-btn:hover {
                background-color: #eaf0ff;
            }
            .nav-title {
                color: white;
                font-weight: 700;
                font-size: 1.1rem;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    col1, col2, col3, col4, col5, col6 = st.columns([2, 1, 1, 1, 1, 1])
    with col1:
        st.markdown('<div class="nav-title">📦 Audit Pack Collector</div>', unsafe_allow_html=True)
    with col2:
        if st.button("🏠 Home", key="home_btn", use_container_width=True):
            go_to("Home")
    with col3:
        if st.button("📁 Upload", key="upload_btn", use_container_width=True):
            go_to("Upload")
    with col4:
        if st.button("📊 Dashboard", key="dashboard_btn", use_container_width=True):
            go_to("Dashboard")
    with col5:
        if st.button("🔐 Login", key="login_btn", use_container_width=True):
            go_to("Login")
    with col6:
        if st.button("🧾 Sign Up", key="signup_btn", use_container_width=True):
            go_to("SignUp")

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
# RENDER NAVBAR
# ---------------------------
navigation_bar()
st.write("")  # small spacer


# ---------------------------
# PAGE CONTENT
# ---------------------------

# HOME PAGE
if st.session_state["page"] == "Home":
    st.markdown("## 👋 Welcome to Audit Pack Collector")
    st.write(
        """
        This platform helps HR and Compliance teams easily track and collect all required audit documents from each department.  
        
        **Key Features**
        - 📋 Centralized checklist  
        - 📁 File upload & tracking  
        - 📊 Real-time progress dashboard  
        - 🔐 Login and role-based access  
        """
    )
    st.image("https://cdn-icons-png.flaticon.com/512/2991/2991106.png", width=200)
    st.info("Use the navigation bar above to explore different pages.")


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
    st.header("📊 Audit Dashboard")

    df = st.session_state.audit_items
    completed = df["Status"].eq("Completed").sum()
    total = len(df)
    progress = (completed / total) * 100

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Departments", df["Department"].nunique())
    col2.metric("Total Items", total)
    col3.metric("Completed", completed)

    st.progress(progress / 100)
    st.caption(f"✅ {progress:.0f}% of audit items completed")

    st.dataframe(df, use_container_width=True)
    st.divider()
    st.caption("💡 This dashboard updates automatically when uploads are completed.")


# LOGIN PAGE
elif st.session_state["page"] == "Login":
    st.header("🔐 Login")

    with st.form("login_form"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")

        if submitted:
            st.success("✅ Logged in (demo only — no backend yet).")


# SIGN UP PAGE
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
                st.success("✅ Account created! (demo only — no backend yet).")
