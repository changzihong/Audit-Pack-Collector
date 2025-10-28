import streamlit as st
import pandas as pd
from datetime import datetime

# ---------------------------
# PAGE CONFIG
# ---------------------------
st.set_page_config(page_title="Audit Pack Collector", layout="wide")

# ---------------------------
# NAVIGATION SETUP
# ---------------------------
def set_page(page_name):
    st.session_state["page"] = page_name

if "page" not in st.session_state:
    st.session_state["page"] = "Home"

# ---------------------------
# NAVBAR
# ---------------------------
st.markdown(
    """
    <style>
    .navbar {
        background-color: #0d6efd;
        padding: 10px 20px;
        border-radius: 6px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .nav-links a {
        color: white;
        margin: 0 10px;
        text-decoration: none;
        font-weight: 500;
    }
    .nav-links a:hover {
        text-decoration: underline;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="navbar">
        <div class="logo" style="color:white; font-weight:bold;">📦 Audit Pack Collector</div>
        <div class="nav-links">
            <a href="?page=Home">Home</a>
            <a href="?page=Upload">Upload</a>
            <a href="?page=Dashboard">Dashboard</a>
            <a href="?page=Login">Login</a>
            <a href="?page=SignUp">Sign Up</a>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# Handle link clicks manually
query_params = st.experimental_get_query_params()
if "page" in query_params:
    st.session_state["page"] = query_params["page"][0]


# ---------------------------
# PAGE LOGIC
# ---------------------------

# --- Dummy data (persistent)
if "audit_items" not in st.session_state:
    st.session_state.audit_items = pd.DataFrame({
        "Department": ["HR", "Finance", "IT", "Operations"],
        "Document": ["Training Records", "Payroll Compliance", "System Access Logs", "Safety Certificates"],
        "Status": ["Pending", "Pending", "Pending", "Pending"],
        "Last Updated": ["", "", "", ""],
    })

# ---------------------------
# HOME PAGE
# ---------------------------
if st.session_state["page"] == "Home":
    st.markdown("## 👋 Welcome to Audit Pack Collector")
    st.write(
        """
        This tool helps HR and Compliance teams collect, track, and manage all required audit documents efficiently.

        **Features:**
        - Centralized audit checklist  
        - Real-time progress tracking  
        - Smart reminders & file uploads  
        - Ready for Supabase integration  
        """
    )
    st.image(
        "https://cdn-icons-png.flaticon.com/512/2991/2991106.png",
        width=200,
    )
    st.info("Use the navigation bar above to explore Upload, Dashboard, or Login/Sign Up pages.")


# ---------------------------
# UPLOAD PAGE
# ---------------------------
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

# ---------------------------
# DASHBOARD PAGE
# ---------------------------
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

# ---------------------------
# LOGIN PAGE
# ---------------------------
elif st.session_state["page"] == "Login":
    st.header("🔐 Login")

    with st.form("login_form"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")

        if submitted:
            st.success("✅ Logged in (demo only — no backend yet).")

# ---------------------------
# SIGNUP PAGE
# ---------------------------
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
