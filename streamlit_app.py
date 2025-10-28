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
# CUSTOM STYLES
# ---------------------------
st.markdown(
    """
    <style>
        /* Navbar container */
        .navbar {
            background-color: white;
            padding: 1rem 1.2rem;
            border-bottom: 1px solid #e5e5e5;
            position: sticky;
            top: 0;
            z-index: 1000;
            text-align: center;
        }

        /* App title */
        .nav-title {
            color: #0d6efd;
            font-weight: 700;
            font-size: 1.3rem;
            margin-bottom: 0.5rem;
        }

        /* Horizontal button container */
        .nav-buttons {
            display: flex;
            justify-content: center;
            gap: 0.8rem;
            flex-wrap: wrap;
        }

        /* Button look */
        div[data-testid="stHorizontalBlock"] button[kind="secondary"] {
            background-color: transparent !important;
            color: #0d6efd !important;
            border: none !important;
            font-weight: 500;
            font-size: 0.95rem;
            transition: all 0.2s ease-in-out;
            border-radius: 6px;
            padding: 0.4rem 1rem;
        }

        div[data-testid="stHorizontalBlock"] button[kind="secondary"]:hover {
            transform: scale(1.05);
            background-color: rgba(13, 110, 253, 0.05) !important;
            box-shadow: 0 1px 3px rgba(0,0,0,0.08);
        }

        /* Reduce default padding */
        .block-container {
            padding-top: 0rem;
        }
    </style>
    """,
    unsafe_allow_html=True
)


# ---------------------------
# NAVIGATION BAR (Centered)
# ---------------------------
def navigation_bar():
    st.markdown(
        """
        <div class="navbar">
            <div class="nav-title">📦 Audit Pack Collector</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Center the buttons using columns
    spacer, col, spacer2 = st.columns([1, 5, 1])
    with col:
        nav_cols = st.columns(5)
        with nav_cols[0]:
            if st.button("🏠 Home", key="home_btn"):
                go_to("Home")
        with nav_cols[1]:
            if st.button("📁 Upload", key="upload_btn"):
                go_to("Upload")
        with nav_cols[2]:
            if st.button("📊 Dashboard", key="dashboard_btn"):
                go_to("Dashboard")
        with nav_cols[3]:
            if st.button("🔐 Login", key="login_btn"):
                go_to("Login")
        with nav_cols[4]:
            if st.button("🧾 Sign Up", key="signup_btn"):
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
# MAIN LAYOUT
# ---------------------------
navigation_bar()
st.markdown("---")  # divider under nav


# ---------------------------
# PAGE CONTENT
# ---------------------------

# HOME PAGE
if st.session_state["page"] == "Home":
    st.markdown("## 👋 Welcome to Audit Pack Collector")
    st.write(
        """
        A modern tool for HR and Compliance teams to collect and track all audit documents efficiently.
        
        **Core Features**
        - 📋 Centralized audit checklist  
        - 📁 File upload & evidence tracking  
        - 📊 Progress visualization  
        - 🔐 Login and sign-up (demo only)
        """
    )
    st.image("https://cdn-icons-png.flaticon.com/512/2991/2991106.png", width=200)
    st.info("Use the navigation bar above to switch pages.")


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
