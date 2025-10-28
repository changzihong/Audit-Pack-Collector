import streamlit as st

# --- PAGE SETUP ---
st.set_page_config(page_title="Audit Pack Collector", layout="wide")

# --- CUSTOM CSS ---
st.markdown("""
    <style>
        /* Remove white space / padding above and below main area */
        .main, .block-container {
            padding-top: 0rem !important;
            padding-bottom: 0rem !important;
            margin-top: 0 !important;
        }

        /* Navbar styling */
        .navbar {
            display: flex;
            justify-content: center;
            align-items: center;
            background-color: #000080;
            padding: 1rem 0;
            width: 100%;
            position: sticky;
            top: 0;
            z-index: 999;
        }

        .nav-item {
            color: #ADD8E6; /* light blue text */
            text-decoration: none;
            margin: 0 1.5rem;
            font-size: 1.1rem;
            font-weight: 600;
            transition: transform 0.2s ease;
        }

        .nav-item:hover {
            transform: scale(1.05);
        }

        /* Active button style */
        .active {
            border-bottom: 2px solid #4CAF50;
        }

        /* Title section */
        .title-section {
            text-align: center;
            margin-top: 2rem;
            margin-bottom: 1.5rem;
        }

        .title-section h1 {
            color: #000080;
            font-size: 2.2rem;
            font-weight: 700;
        }

        /* Page content */
        .content {
            background-color: #F5F5F5;
            padding: 2rem 4rem;
            border-radius: 12px;
            margin: 1rem auto;
            width: 85%;
            box-shadow: 0px 4px 8px rgba(0,0,0,0.05);
        }

        /* Button styling for Login/Signup */
        .nav-btn {
            background-color: transparent;
            border: none;
            color: #ADD8E6;
            font-size: 1.1rem;
            font-weight: 600;
            cursor: pointer;
            margin: 0 1.5rem;
            transition: transform 0.2s ease;
        }

        .nav-btn:hover {
            transform: scale(1.05);
        }
    </style>
""", unsafe_allow_html=True)

# --- NAVIGATION STATE ---
if "page" not in st.session_state:
    st.session_state.page = "Home"

# --- NAVBAR ---
st.markdown("""
<div class="navbar">
    <button class="nav-btn" onclick="window.location.href='/?page=Home'">Home</button>
    <button class="nav-btn" onclick="window.location.href='/?page=Login'">Login</button>
    <button class="nav-btn" onclick="window.location.href='/?page=SignUp'">SignUp</button>
</div>
""", unsafe_allow_html=True)

# --- URL PARAMETER DETECTION ---
query_params = st.query_params
page = query_params.get("page", ["Home"])[0]

# --- PAGE CONTENT ---
st.markdown(f"<div class='title-section'><h1>Welcome to Audit Pack Collector</h1></div>", unsafe_allow_html=True)

if page == "Home":
    st.markdown("""
        <div class="content">
            <h3>📂 About the System</h3>
            <p>This app helps HR teams organize, track, and validate all required audit documents efficiently.</p>
            <ul>
                <li>Secure central repository for all audit files</li>
                <li>Built-in document checklist</li>
                <li>Role-based responsibility tracker</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

elif page == "Login":
    st.markdown("""
        <div class="content">
            <h3>🔐 Login</h3>
            <p>Enter your credentials to access your audit workspace.</p>
        </div>
    """, unsafe_allow_html=True)

elif page == "SignUp":
    st.markdown("""
        <div class="content">
            <h3>📝 Sign Up</h3>
            <p>Create a new account to start managing your HR audit documents.</p>
        </div>
    """, unsafe_allow_html=True)
