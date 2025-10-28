import streamlit as st
import pandas as pd
from datetime import datetime

# ---------------------------
# PAGE CONFIG
# ---------------------------
st.set_page_config(page_title="Audit Pack Collector", layout="wide", page_icon="📂")

# ---------------------------
# SESSION STATE
# ---------------------------
if "page" not in st.session_state:
    st.session_state["page"] = "🏠 Home"

def go_to(page):
    st.session_state["page"] = page


# ---------------------------
# GLOBAL STYLES (Luxury Theme)
# ---------------------------
st.markdown("""
<style>
/* Remove default padding */
.block-container { padding-top: 0 !important; }

/* Background gradient */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #f8f9fb 0%, #e9efff 100%);
}

/* ===========================
   NAVBAR
   =========================== */
.navbar {
    background: linear-gradient(90deg, #001f54 0%, #003366 100%);
    padding: 1rem 2rem;
    border-bottom: 3px solid #FFD700;
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    position: sticky;
    top: 0;
    z-index: 999;
    text-align: center;
}

/* Navbar title */
.nav-title {
    color: #FFD700;
    font-weight: 800;
    font-size: 1.6rem;
    letter-spacing: 0.6px;
}

/* Nav buttons */
.stButton>button {
    background: transparent !important;
    color: #FFD700 !important;
    border: 1px solid transparent !important;
    font-weight: 600;
    border-radius: 6px;
    padding: 0.4rem 1rem;
    transition: all 0.3s ease;
}
.stButton>button:hover {
    transform: scale(1.07);
    background-color: rgba(255,255,255,0.1) !important;
    border-color: rgba(255,255,255,0.2) !important;
}
button[data-active="true"] {
    background: #FFD700 !important;
    color: #001f54 !important;
}

/* ===========================
   MAIN CONTENT
   =========================== */
.main-wrapper {
    margin: 2rem auto;
    padding: 2.5rem 3rem;
    width: 88%;
    background: rgba(255, 255, 255, 0.85);
    backdrop-filter: blur(10px);
    border-radius: 18px;
    box-shadow: 0 6px 20px rgba(0,0,0,0.08);
}

/* Headings */
h2, h3 {
    color: #001f54 !important;
}

/* Progress bar */
[data-testid="stProgressBar"] div[role="progressbar"] {
    background: linear-gradient(90deg, #4CAF50, #8BC34A);
}

/* Metric text color */
[data-testid="stMetricValue"] { color: #001f54; font-weight: 700; }

/* Table */
[data-testid="stDataFrame"] table {
    border-radius: 8px;
    overflow: hidden;
    background-color: #fff;
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
    </div>
    """, unsafe_allow_html=True)

    pages = ["🏠 Home", "📤 Upload", "📊 Dashboard", "🔐 Login", "🧾 SignUp"]
    cols = st.columns(len(pages))
    for i, page in enumerate(pages):
        with cols[i]:
            active = "true" if st.session_state["page"] == page else "false"
            if st.button(page, key=f"nav_{page}", use_container_width=True):
                go_to(page)
            st.markdown(
                f"<script>document.querySelector('[key=\"nav_{page}\"] button').setAttribute('data-active', '{active}')</script>",
                unsafe_allow_html=True
            )


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
# PAGE CONTENT
# ---------------------------
navigation_bar()

with st.container():
    st.markdown('<div class="main-wrapper">', unsafe_allow_html=True)

    # HOME PAGE
    if st.session_state["page"] == "🏠 Home":
        st.markdown("## 👋 Welcome to Audit Pack Collector")
        st.write("""
        A demo platform designed for HR and Compliance teams to efficiently manage audit documentation.  
        Sleek, smart, and ready for enterprise — even in demo mode.

        **Key Highlights**
        - 🗂️ Central Repository for all evidence  
        - ✅ Checklist & Tracking Dashboard  
        - 🤖 Mock AI Insights for smarter prioritization  
        - 🧾 Simple Upload & Auto Status Update
        """)
        st.image("https://cdn-icons-png.flaticon.com/512/2991/2991106.png", width=200)
        st.success("Use the navigation bar above to explore modules.")

    # UPLOAD PAGE
    elif st.session_state["page"] == "📤 Upload":
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
    elif st.session_state["page"] == "📊 Dashboard":
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

        st.subheader("🤖 AI Assistant Insight (Demo)")
        if progress < 100:
            st.info("AI suggests: Focus on uploading missing *Safety Certificates* to reach full compliance this week.")
        else:
            st.success("AI confirms: All departments are fully compliant! Great job 🎯")

        if st.button("📄 Export Audit Summary (Demo)"):
            st.success("✅ Audit Summary generated successfully (demo only).")

    # LOGIN PAGE
    elif st.session_state["page"] == "🔐 Login":
        st.header("🔐 Login (Demo)")
        with st.form("login_form"):
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Login")
            if submitted:
                st.success("✅ Logged in (demo only — no backend connected).")

    # SIGNUP PAGE
    elif st.session_state["page"] == "🧾 SignUp":
        st.header("🧾 Create an Account (Demo)")
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
                    st.success("✅ Account created successfully (demo only).")

    st.markdown("</div>", unsafe_allow_html=True)
