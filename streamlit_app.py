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

def go_to(page_name):
    st.session_state["page"] = page_name


# ---------------------------
# NAVIGATION BAR
# ---------------------------
def navigation_bar():
    st.markdown(
        """
        <style>
            .navbar {
                background-color: white;
                padding: 0.8rem 1.2rem;
                border-bottom: 1px solid #e5e5e5;
                display: flex;
                justify-content: space-between;
                align-items: center;
                position: sticky;
                top: 0;
                z-index: 999;
            }
            .nav-title {
                color: #0d6efd;
                font-weight: 700;
                font-size: 1.2rem;
            }
            .nav-btn {
                background: none;
                color: #0d6efd;
                border: none;
                font-weight: 500;
                font-size: 0.95rem;
                margin-left: 0.5rem;
                cursor: pointer;
                transition: all 0.2s ease-in-out;
                border-radius: 6px;
                padding: 0.4rem 0.9rem;
            }
            .nav-btn:hover {
                transform: scale(1.05);
                background-color: rgba(13, 110, 253, 0.05);
                box-shadow: 0 1px 3px rgba(0,0,0,0.08);
            }
        </style>

        <div class="navbar">
            <div class="nav-title">📦 Audit Pack Collector</div>
            <div>
                <form action="#" method="get" style="display:inline;">
                    <button class="nav-btn" type="submit" formaction="?page=Home">🏠 Home</button>
                    <button class="nav-btn" type="submit" formaction="?page=Upload">📁 Upload</button>
                    <button class="nav-btn" type="submit" formaction="?page=Dashboard">📊 Dashboard</button>
                    <button class="nav-btn" type="submit" formaction="?page=Login">🔐 Login</button>
                    <button class="nav-btn" type="submit" formaction="?page=SignUp">🧾 Sign Up</button>
                </form>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


# ---------------------------
# URL HANDLING (simulate navigation)
# ---------------------------
query_params = st.query_params
if "page" in query_params:
    st.session_state["page"] = query_params["page"]

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
st.write("")


# ---------------------------
# PAGE CONTENTS
# ---------------------------

# HOME PAGE
if st.session_state["page"] == "Home":
    st.markdown("## 👋 Welcome to Audit Pack Collector")
    st.write(
        """
        A lightweight audit document collection dashboard for HR and Compliance teams.
        
        **Features**
        - Centralized checklist  
        - File uploads with status tracking  
        - Real-time dashboard  
        - Secure login system (coming soon)
        """
    )
    st.image("https://cdn-icons-png.flaticon.com/512/2991/2991106.png", width=200)
    st.info("Use the navigation bar to explore other sections.")


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
    col1.metric("Departments", df["Department"].nunique())
    col2.metric("Total Items", total)
    col3.metric("Completed", completed)

    st.progress(progress / 100)
    st.caption(f"✅ {progress:.0f}% of audit items completed")

    st.dataframe(df, use_container_width=True)
    st.divider()
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
                st.success("✅ Account created (demo only — backend not connected).")
