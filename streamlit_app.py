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
# CSS STYLES
# ---------------------------
st.markdown("""
<style>
/* General layout reset */
.block-container {
    padding-top: 0 !important;
}

/* Remove extra markdown white space */
[data-testid="stMarkdownContainer"] {
    margin: 0 !important;
    padding: 0 !important;
}

/* Hide any empty Streamlit wrappers */
.element-container:has(.main-wrapper:empty),
[data-testid="stElementContainer"]:has(.main-wrapper:empty) {
    display: none !important;
}

/* Background color */
[data-testid="stAppViewContainer"] {
    background-color: #F5F5F5;
}

/* Navbar */
.navbar {
    background-color: #000080;
    padding: 1rem 1.5rem;
    box-shadow: 0 2px 6px rgba(0,0,0,0.1);
    text-align: center;
    position: sticky;
    top: 0;
    z-index: 100;
}

.nav-title {
    color: #99CCFF;
    font-weight: 700;
    font-size: 1.4rem;
    letter-spacing: 0.5px;
}

.nav-buttons {
    display: flex;
    justify-content: center;
    gap: 1rem;
    margin-top: 0.6rem;
}

.stButton>button {
    background-color: transparent !important;
    color: #99CCFF !important;
    border: 1px solid transparent !important;
    border-radius: 6px;
    font-weight: 500;
    padding: 0.4rem 1rem;
    transition: all 0.25s ease;
}

.stButton>button:hover {
    transform: scale(1.07);
    background-color: rgba(153,204,255,0.12) !important;
    border-color: rgba(153,204,255,0.4) !important;
}

/* Active page button */
button[data-active="true"] {
    background-color: #99CCFF !important;
    color: #000080 !important;
    font-weight: 600 !important;
}

/* Divider line */
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

/* Auth container (Login / Signup) */
.auth-container {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 80vh;
}

.auth-card {
    width: 420px;
    background-color: white;
    border-radius: 14px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.1);
    padding: 2rem;
    text-align: center;
}

.auth-card h2 {
    color: #000080;
    margin-bottom: 1rem;
    font-weight: 700;
}

.auth-btn > button {
    background-color: #000080 !important;
    color: #FFFFFF !important;
    border-radius: 6px !important;
    padding: 0.6rem 1rem !important;
    font-weight: 600 !important;
    width: 100%;
    transition: all 0.25s ease;
}

.auth-btn > button:hover {
    transform: scale(1.05);
    box-shadow: 0 0 10px rgba(153, 204, 255, 0.5);
}

/* Link style */
.auth-link {
    color: #000080;
    text-decoration: underline;
    cursor: pointer;
    font-size: 0.9rem;
}
.auth-link:hover {
    color: #4CAF50;
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
            active = "true" if st.session_state["page"] == page else "false"
            if st.button(page, key=f"nav_{page}", use_container_width=True):
                go_to(page)
            st.markdown(
                f"<script>document.querySelector('[key=\"nav_{page}\"] button').setAttribute('data-active', '{active}')</script>",
                unsafe_allow_html=True
            )

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
# PAGE CONTENT
# ---------------------------
navigation_bar()

# LOGIN PAGE
if st.session_state["page"] == "Login":
    st.markdown('<div class="auth-container"><div class="auth-card">', unsafe_allow_html=True)
    st.markdown("## 🔐 Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Login", key="login_btn", use_container_width=True):
        st.success("✅ Logged in (demo only).")
    st.markdown('<p style="margin-top:1rem;">No account? <span class="auth-link" onClick="window.parent.location.reload()">Sign Up</span></p>', unsafe_allow_html=True)
    st.markdown("</div></div>", unsafe_allow_html=True)

# SIGN UP PAGE
elif st.session_state["page"] == "SignUp":
    st.markdown('<div class="auth-container"><div class="auth-card">', unsafe_allow_html=True)
    st.markdown("## 🧾 Create an Account")
    name = st.text_input("Full Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    confirm = st.text_input("Confirm Password", type="password")
    if st.button("Sign Up", key="signup_btn", use_container_width=True):
        if password != confirm:
            st.error("❌ Passwords do not match.")
        else:
            st.success("✅ Account created (demo only).")
    st.markdown('<p style="margin-top:1rem;">Already have an account? <span class="auth-link" onClick="window.parent.location.reload()">Login here</span></p>', unsafe_allow_html=True)
    st.markdown("</div></div>", unsafe_allow_html=True)

# MAIN CONTENT PAGES
else:
    st.markdown('<div class="main-wrapper">', unsafe_allow_html=True)

    if st.session_state["page"] == "Home":
        st.markdown("## 👋 Welcome to Audit Pack Collector")
        st.write("This system helps HR and Compliance teams compile, track, and review audit documents efficiently.")
        st.image("https://cdn-icons-png.flaticon.com/512/2991/2991106.png", width=200)
        st.info("Use the navigation bar to explore modules.")

    elif st.session_state["page"] == "Upload":
        st.header("📁 Upload Audit Evidence")
        dept = st.selectbox("Select Department", st.session_state.audit_items["Department"])
        doc_type = st.selectbox("Select Document Type",
                                st.session_state.audit_items.query("Department == @dept")["Document"])
        uploaded_file = st.file_uploader("Upload File", type=["pdf", "docx", "jpg", "png"])
        if uploaded_file:
            st.success(f"✅ File '{uploaded_file.name}' uploaded for {dept} - {doc_type}")
            idx = st.session_state.audit_items.query("Department == @dept and Document == @doc_type").index[0]
            st.session_state.audit_items.loc[idx, "Status"] = "Completed"
            st.session_state.audit_items.loc[idx, "Last Updated"] = datetime.now().strftime("%Y-%m-%d %H:%M")

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

    st.markdown("</div>", unsafe_allow_html=True)
